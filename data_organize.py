import pandas as pd
import numpy as np

import glob
from sqlite3 import connect
import time
import datetime
from pprint import pprint
import re
import os
import string
from helpers import load_masterdictionary

import constants as C

RE_DOCUMENT = re.compile(r"<DOCUMENT>([\w\W]*?)</DOCUMENT>", re.MULTILINE)


SQL_SELECT_JOIN_MASTER = """

SELECT master.`index`, master.cik, ccm_lookup.lpermno, ccm_lookup.gvkey, master.name, master.form, master.filingdate, master.url, master.fname
FROM master
INNER JOIN ccm_lookup ON ccm_lookup.cik=master.cik;

"""

def edit_master(MAIN, PERMNO):
    master = pd.read_sql(SQL_SELECT_JOIN_MASTER, MAIN, index_col='index')
    
    master['lpermno'] = master['lpermno'].astype('Int32')
    master['filingdate'] = pd.to_datetime(master['filingdate'], format='%Y%m%d')
    
    lm_dictionary = load_masterdictionary(C.MASTER_DICT_PATH)

    book_value_df = pd.read_csv('book_value.csv', index_col=None, header=0, sep=',', dtype=str)

    cur = MAIN.cursor()
    res = cur.execute("SELECT SIC, FF_NUMBER FROM sic_mapping")
    sic_mapping = {r[0]: r[1] for r in res.fetchall()}

    edited_master = master.apply(lambda master_row: apply_dict(get_data_dict, master_row, book_value_df, sic_mapping, lm_dictionary, MAIN, PERMNO), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')



def apply_dict(callback, *args, **kwargs):
    data = callback(*args, **kwargs)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def get_data_dict(master_row, book_value_df, sic_mapping, lm_dictionary, MAIN, PERMNO):
    financial_data = {
        'price_minus_one_day': None, 
        'volume_minus_one_day': None,
        'shares_outstanding_minus_one_day': None,
        'ff_industry': None,
        'median_filing_period_returns': None, 
        'median_filing_period_value_weighted_returns': None,
        'turnover': None,
        'book_value_per_share': None,
        'quater': int(master_row['fname'][3:4]),
        'year': int(master_row['fname'][5:9]),
    }
    financial_columns_count = len(financial_data.keys())
    _fill_financial_data(financial_data, master_row, book_value_df, sic_mapping, MAIN, PERMNO)
    assert len(financial_data.keys()) == financial_columns_count

    textual_data = {
        'file_size': 0, # 1
        'number_of_words': 0, # 2
        'percent_positive': 0, # 3
        'percent_negative': 0, # 4
        'percent_uncertainty': 0, # 5
        'percent_litigious': 0, # 6
        'percent_modal_weak': 0, # 7
        'percent_modal_moderate': 0, # 8
        'percent_modal_strong': 0, # 9
        'percent_constraining': 0, # 10
        'number_of_alphabetic': 0, # 11
        'number_of_digits': 0, # 12
        'number_of_numbers': 0, # 13
        'avg_number_of_syllables_per_word': 0, # 14
        'average_word_length': 0, # 15
        'vocabulary': 0, # 16
    }
    fname_path = os.path.join('parsed', str(financial_data['year']), master_row['fname'])
    textual_columns_count = len(textual_data.keys())
    _fill_textual_data(textual_data, fname_path, master_row, lm_dictionary)
    assert len(textual_data.keys()) == textual_columns_count

    data = {}
    data.update(financial_data)
    data.update(textual_data)
    return data


def _fill_textual_data(row, fname, master_row, lm_dictionary):
    if not os.path.isfile(fname):
        print("File missing: ", fname)
        return

    with open(fname, 'r', encoding='UTF-8', errors='ignore') as f_in:
        doc = f_in.read()

    row['file_size'] = len(doc)
    doc = doc.upper()  # for this parse caps aren't informative so shift
    doc = re.sub(r'\sMAY\s', ' ', doc)  # drop all May month references
    doc = RE_DOCUMENT.search(doc).group(1) # Drop SIC header and FILESTATS tags

    vdictionary = {}
    total_syllables = 0
    word_length = 0
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            row['number_of_words'] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: row['percent_positive'] += 1
            if lm_dictionary[token].negative: row['percent_negative'] += 1
            if lm_dictionary[token].uncertainty: row['percent_uncertainty'] += 1
            if lm_dictionary[token].litigious: row['percent_litigious'] += 1
            if lm_dictionary[token].weak_modal: row['percent_modal_weak'] += 1
            if lm_dictionary[token].moderate_modal: row['percent_modal_moderate'] += 1
            if lm_dictionary[token].strong_modal: row['percent_modal_strong'] += 1
            if lm_dictionary[token].constraining: row['percent_constraining'] += 1
            total_syllables += lm_dictionary[token].syllables

    row['number_of_alphabetic'] = len(re.findall('[A-Z]', doc))
    row['number_of_digits'] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    row['number_of_numbers'] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    if not row['number_of_words']:
        return
    row['vocabulary'] = len(vdictionary)
    row['avg_number_of_syllables_per_word'] = total_syllables / row['number_of_words']
    row['average_word_length'] = word_length / row['number_of_words']
    
    # Convert counts to %
    for column_name in row:
        if column_name.startswith('percent_'):
            row[column_name] = (row[column_name] / row['number_of_words']) * 100
        
    return


def _fill_financial_data(data, master_row, book_value_df, sic_mapping, MAIN, PERMNO):
    permno = master_row['lpermno']

    if not permno or not perm_number_table_exists(PERMNO, permno):
        # No stock data at all
        return

    df = pd.read_sql("select * from '%s'" % permno, PERMNO, index_col='rowid')
    df['RET'] = pd.to_numeric(df['RET'], errors='coerce')
    df['VOL'] = pd.to_numeric(df['VOL'], errors='coerce')

    before = len(df.index)
    df = df[df['RET'] > -0.66]
    df = df[np.isfinite(df['VOL'])]
    after = len(df.index)
    if before != after:
        print("Lines remaining %s/%s" % (after, before))
        print(df)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    sub_df = df.loc[df['date'] == master_row['filingdate']]

    if len(sub_df) == 0:
        # No stock data on filing date
        return 

    row = sub_df.iloc[0]
    idx = df.index.get_loc(row.name)
    history = df.iloc[idx - 60 : idx + 60]
    prc = df.iloc[idx-1]['PRC']

    VOL = df.iloc[idx-1]['VOL']
    SHROUT = df.iloc[idx-1]['SHROUT']

    data['price_minus_one_day'] = float(prc) if prc else None
    data['volume_minus_one_day'] = int(VOL) if VOL else None
    data['shares_outstanding_minus_one_day'] = int(SHROUT) if SHROUT else None
    data['ff_industry'] = sic_mapping.get(df.iloc[idx-1]['SICCD'])
    data['median_filing_period_returns'] = df.iloc[idx:idx+4]['RET'].median(axis=0)
    data['median_filing_period_value_weighted_returns'] = df.iloc[idx:idx+4]['vwretd'].median(axis=0)

    history = df.iloc[idx - 252 : idx -6]
    FILING_DATE_SHROUT = df.iloc[idx]['SHROUT']
    # The volume of shares traded in days [−252,−6] prior to thefile date divided by shares outstanding on the file date. 
    # Atleast 60 observations of daily volume must be available to be included in the sample.
    if len(history) < 60 or not SHROUT:
        data['turnover'] = None
    else:
        data['turnover'] = history['VOL'].sum(axis=0) / float(FILING_DATE_SHROUT)

    import pdb; pdb.set_trace()
    # Book-to-market COMPUSTAT data available
    company_values = book_value_df.loc[book_value_df['gvkey'] == master_row['gvkey']].loc[book_value_df['fyear'] == str(data['year'])]
    if len(company_values) == 0:
        return

    row = company_values.iloc[0]
    data['book_value_per_share'] = row['bkvlps']




def create_company_tables(MAIN, PERMNO):
    main_cur = MAIN.cursor()
    print("Creating index for PERMNO to make future queries faster.")
    main_cur.execute("CREATE INDEX IF NOT EXISTS permno_idx ON all_stocks(PERMNO)")
    print("Query for unique PERMNO's")
    res = main_cur.execute("SELECT DISTINCT PERMNO from all_stocks").fetchall()
    perm_numbers = set(t[0] for t in res)
    print("Unique PERMNO's: ", len(perm_numbers))
    perm_cur = PERMNO.cursor()
    for perm_no in perm_numbers:
        create_based_on_permno(MAIN, PERMNO, perm_no)
        perm_cur.execute("CREATE INDEX IF NOT EXISTS date_idx ON `%s`(date)" % perm_no)


def perm_number_table_exists(PERMNO, perm_no):
    cur = PERMNO.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % perm_no)
    return bool(res.fetchall())

def create_based_on_permno(MAIN, PERMNO, perm_no):
    if perm_number_table_exists(PERMNO, perm_no):
        print("Table exists ", perm_no)
        return 
    print("Create table for ", perm_no)
    df = pd.read_sql("select rowid, * from all_stocks where PERMNO='%s'" % perm_no, MAIN, index_col='rowid')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

    df = df.drop('PERMNO', axis=1)
    df.to_sql(name=perm_no, con=PERMNO, if_exists='fail')



def main():
    with connect(C.MAIN_DB_NAME) as MAIN, connect(C.PERMNO_DB_NAME) as PERMNO:
        # create_company_tables(MAIN, PERMNO)
        edit_master(MAIN, PERMNO)

if __name__ == '__main__':
    main()
