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

import constants as C

RE_DOCUMENT = re.compile(r"<DOCUMENT>([\w\W]*?)</DOCUMENT>", re.MULTILINE)


DT_FORMAT = '%Y-%m-%d %H:%M:%S'

SQL_SELECT_JOIN_MASTER = """

SELECT master.`index`, master.cik, ccm_lookup.lpermno, ccm_lookup.gvkey, master.name, master.form, master.filingdate, master.url, master.fname
FROM master
INNER JOIN ccm_lookup ON ccm_lookup.cik=master.cik WHERE ccm_lookup.lpermno IS NOT NULL;


"""

SQL_PERMNO_INDEX = """

CREATE INDEX permno_idx 
ON all_stocks(PERMNO); 

"""

def edit_master(MAIN, PERMNO):
    master = pd.read_sql(SQL_SELECT_JOIN_MASTER, MAIN, index_col='index')
    master['lpermno'] = master['lpermno'].apply(lambda x: int(x))
    master['filingdate'] = pd.to_datetime(master['filingdate'], format='%Y%m%d')

    edited_master = master.apply(lambda row: apply_master(row, MAIN, PERMNO, len(master)), axis=1)
    joined = pd.concat([master, edited_master], axis=1)
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')

def parse_files(MAIN):
    from helpers import load_masterdictionary
    master = pd.read_sql("select rowid, * from master_edited", MAIN, index_col='rowid')
    lm_dictionary = load_masterdictionary(C.MASTER_DICT_PATH)


    edited_master = master.apply(lambda row: apply_master_file_data(row, lm_dictionary), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_parsed', con=MAIN, if_exists='replace')


def _master_fill_from_permno(data, master_row, PERMNO):
    permno = master_row['lpermno']

    if not perm_number_table_exists(PERMNO, permno):
        return
    df = pd.read_sql("select * from '%s'" % permno, PERMNO, index_col='rowid')
    df['RET'] = pd.to_numeric(df['RET'], errors='coerce')
    before = len(df.index)
    df = df[df['RET'] > -0.66]
    after = len(df.index)
    if before != after:
        print("Lines remaining %s/%s" % (after, before))
        print(df)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    sub_df = df.loc[df['date'] == master_row['filingdate']]

    if len(sub_df) == 0:
        return 

    row = sub_df.iloc[0]
    idx = df.index.get_loc(row.name)
    history = df.iloc[idx - 60 : idx + 60]
    prc = df.iloc[idx-1]['PRC']

    VOL = df.iloc[idx-1]['VOL']
    SHROUT = df.iloc[idx-1]['SHROUT']

    data['price_minus_one_day'] = float(prc) if prc else None
    data['sixty_days_trading'] = len(history) == 120
    data['volume'] = int(VOL) if VOL else None
    data['shares_outstanding'] = int(SHROUT) if SHROUT else None
    data['SICCD'] = df.iloc[idx-1]['SICCD']
    data['median_RET'] = df.iloc[idx:idx+4]['RET'].median(axis=0)
    data['median_vwretd'] = df.iloc[idx:idx+4]['vwretd'].median(axis=0)



def apply_master(master_row, MAIN, PERMNO, n_rows):
    print("Processing row %s/%s" % (master_row.name, n_rows))

    data = {
        'price_minus_one_day': None,
        'sixty_days_trading': None,
        'volume': None,
        'shares_outstanding': None,
        'SICCD': None,
        'median_RET': None,
        'median_vwretd': None,
    }

    _master_fill_from_permno(data, master_row, PERMNO)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def read_master(MAIN):
    return pd.read_sql("select * from master_joined", MAIN, index_col='index')


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


def apply_master_file_data(master_row, lm_dictionary):
    fname = master_row['fname']
    year = master_row['filingdate'][:4]
    path = os.path.join('parsed', year, fname)
    data = get_file_data(path, lm_dictionary)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def get_file_data(fname, lm_dictionary):
    row = {
        'file size': 0, # 1
        'number of words': 0, # 2
        '% positive': 0, # 3
        '% negative': 0, # 4
        '% uncertainty': 0, # 5
        '% litigious': 0, # 6
        '% modal-weak': 0, # 7
        '% modal moderate': 0, # 8
        '% modal strong': 0, # 9
        '% constraining': 0, # 10
        '# of alphabetic': 0, # 11
        '# of digits': 0, # 12
        '# of numbers': 0, # 13
        'avg # of syllables per word': 0, # 14
        'average word length': 0, # 15
        'vocabulary': 0, # 16
    }

    if not os.path.isfile(fname):
        print("File missing: ", fname)
        return row

    with open(fname, 'r', encoding='UTF-8', errors='ignore') as f_in:
        doc = f_in.read()

    row['file size'] = len(doc)
    doc = doc.upper()  # for this parse caps aren't informative so shift
    doc = re.sub(r'\sMAY\s', ' ', doc)  # drop all May month references
    doc = RE_DOCUMENT.search(doc).group(1) # Drop SIC header and FILESTATS tags

    vdictionary = {}
    total_syllables = 0
    word_length = 0
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            row['number of words'] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: row['% positive'] += 1
            if lm_dictionary[token].negative: row['% negative'] += 1
            if lm_dictionary[token].uncertainty: row['% uncertainty'] += 1
            if lm_dictionary[token].litigious: row['% litigious'] += 1
            if lm_dictionary[token].weak_modal: row['% modal-weak'] += 1
            if lm_dictionary[token].moderate_modal: row['% modal moderate'] += 1
            if lm_dictionary[token].strong_modal: row['% modal strong'] += 1
            if lm_dictionary[token].constraining: row['% constraining'] += 1
            total_syllables += lm_dictionary[token].syllables

    row['# of alphabetic'] = len(re.findall('[A-Z]', doc))
    row['# of digits'] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    row['# of numbers'] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    if not row['number of words']:
        return row
    row['vocabulary'] = len(vdictionary)
    row['avg # of syllables per word'] = total_syllables / row['number of words']
    row['average word length'] = word_length / row['number of words']
    
    # Convert counts to %
    for column_name in row:
        if column_name.startswith('%'):
            row[column_name] = (row[column_name] / row['number of words']) * 100
        
    return row

def apply_book_value_and_ff_industry(master_row, book_value_df, sic_mapping):
    data = get_book_value_data_and_ff_industry(master_row, book_value_df, sic_mapping)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def get_book_value_data_and_ff_industry(master_row, book_value_df, sic_mapping):
    data = {
        'bkvlps': None,
        'ff_industry': sic_mapping.get(master_row['SICCD'], None),
    }
    year = master_row['filingdate'][:4]
    company_values = book_value_df.loc[book_value_df['gvkey'] == master_row['gvkey']].loc[book_value_df['fyear'] == year]
    if len(company_values) == 0:
        return data

    row = company_values.iloc[0]
    data['bkvlps'] = row['bkvlps']

    return data

    


def parse_book_value_and_ff_industry(MAIN):
    master = pd.read_sql("select * from master_parsed", MAIN, index_col='rowid')
    cur = MAIN.cursor()
    res = cur.execute("SELECT SIC, FF_NUMBER FROM sic_mapping")
    sic_mapping = {r[0]: r[1] for r in res.fetchall()}
    book_value_df = pd.read_csv('book_value.csv', index_col=None, header=0, sep=',', dtype=str)

    edited_master = master.apply(lambda row: apply_book_value_and_ff_industry(row, book_value_df, sic_mapping), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_book', con=MAIN, if_exists='replace')




def get_industry_retuns(master_row, industry_df):
    data = {
        'median_industry_returns': None,
    }
    if not master_row['ff_industry']:
        return data

    sub_df = industry_df.loc[industry_df['Date'] == master_row['filingdate']]

    if len(sub_df) == 0:
        return 

    row = sub_df.iloc[0]
    idx = industry_df.index.get_loc(row.name)

    filing_returns_period = industry_df.iloc[idx:idx+4]

    data['median_industry_returns'] = filing_returns_period[master_row['ff_industry']].median(axis=0)

    return data




def apply_industry_returns(master_row, industry_df):
    data = get_industry_retuns(master_row, industry_df)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))




def add_industry_returns(MAIN):
    industry_df = pd.read_csv('industry_numbered_columns.csv', index_col=None, header=0, sep=',', dtype=str)
    industry_df['Date'] = pd.to_datetime(industry_df['Date'], format='%Y%m%d')
    industry_df.sort_values(by=['Date'], inplace=True)


    master = pd.read_sql("select * from master_book", MAIN, index_col='rowid')

    edited_master = master.apply(lambda row: apply_industry_returns(row, industry_df), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')



def add_turnover(MAIN, PERMNO):
    master = pd.read_sql("select * from master_edited", MAIN, index_col='rowid')

    edited_master = master.apply(lambda row: apply_turnover(row, PERMNO), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')



def apply_turnover(master_row, PERMNO):
    data = get_turnover_data(master_row, PERMNO)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def get_turnover_data(master_row, PERMNO):
    data = {
        'turnover': None
    }
    permno = master_row['lpermno']

    if not perm_number_table_exists(PERMNO, permno):
        return data
    df = pd.read_sql("select * from '%s'" % permno, PERMNO, index_col='rowid')
    df['VOL'] = pd.to_numeric(df['VOL'], errors='coerce')
    before = len(df.index)
    df = df[np.isfinite(df['VOL'])]
    after = len(df.index)
    if before != after:
        print("Lines remaining %s/%s" % (after, before))
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    sub_df = df.loc[df['date'] == master_row['filingdate']]

    if len(sub_df) == 0:
        return data

    row = sub_df.iloc[0]
    idx = df.index.get_loc(row.name)

    history = df.iloc[idx - 252 : idx -6]
    SHROUT = df.iloc[idx]['SHROUT']

    if len(history) < 60 or not SHROUT:
        return data

    # The volume of shares traded in days [−252,−6] prior to thefile date divided by shares outstanding on the file date. 
    # Atleast 60 observations of daily volume must be available to be included in the sample.
    data['turnover'] = history['VOL'].sum(axis=0) / float(SHROUT)

    return data





def main():
    with connect(C.MAIN_DB_NAME) as MAIN, connect(C.PERMNO_DB_NAME) as PERMNO:
        # create_company_tables(MAIN, PERMNO)
        # edit_master(MAIN, PERMNO)
        # parse_files(MAIN)
        # parse_book_value_and_ff_industry(MAIN)
        # add_industry_returns(MAIN)
        add_turnover(MAIN, PERMNO)

if __name__ == '__main__':
    main()