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
from scipy import stats

import constants as C

from permno_tables import perm_number_table_exists

RE_DOCUMENT = re.compile(r"<DOCUMENT>([\w\W]*?)</DOCUMENT>", re.MULTILINE)

def edit_master(MAIN, PERMNO):
    master = pd.read_sql("select * from master", MAIN, index_col='index')
    assert len(master) == 114186

    master['filingdate'] = pd.to_datetime(master['filingdate'], format='%Y%m%d')

    ccmlinktable = pd.read_csv('ccmlinktable.csv', index_col=None, header=0, sep=',', dtype=str)
    ccmlinktable['LINKDT'] = pd.to_datetime(ccmlinktable['LINKDT'], format='%Y%m%d')
    #  E means that its valid currently so change that to 2050 so we can do datetime comparisons
    ccmlinktable.LINKENDDT = ccmlinktable.LINKENDDT.replace({"E": "20500101"})
    ccmlinktable['LINKENDDT'] = pd.to_datetime(ccmlinktable['LINKENDDT'], format='%Y%m%d')
    ccmlinktable['LPERMNO'] = ccmlinktable['LPERMNO'].fillna(0).astype(int)
    ccmlinktable['LPERMCO'] = ccmlinktable['LPERMCO'].fillna(0).astype(int)

    # Remove links that have expired before 2008 for performance
    ccmlinktable[(ccmlinktable['LINKENDDT'] > '2007-12-01 00:00:00')]

    lm_dictionary = load_masterdictionary(C.MASTER_DICT_PATH)

    book_value_df = pd.read_csv('book_value.csv', index_col=None, header=0, sep=',', dtype=str)

    cur = MAIN.cursor()
    res = cur.execute("SELECT SIC, FF_CATEGORY FROM sic_mapping")
    sic_mapping = {r[0]: r[1] for r in res.fetchall()}


    market_df = pd.read_csv('market_index.csv', index_col=None, header=0, sep=',', dtype=str)
    market_df['DATE'] = pd.to_datetime(market_df['DATE'], format='%Y%m%d')
    market_df['vwretd'] = pd.to_numeric(market_df['vwretd'], errors='coerce')
    market_df.rename(
        columns={'DATE': 'market_date'},
        inplace=True
    )

    callback_args = (
        book_value_df,
        sic_mapping,
        lm_dictionary,
        ccmlinktable,
        market_df,
        PERMNO,
    )

    edited_master = master.apply(lambda master_row: apply_dict(get_data_dict, master_row, *callback_args), axis=1)

    joined = pd.concat([master, edited_master], axis=1)
    if len(joined.index) != len(master.index):
        # Something wrong with the join
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')



def apply_dict(callback, *args, **kwargs):
    data = callback(*args, **kwargs)

    pprint(data)

    return pd.Series(list(data.values()), index=list(data.keys()))


def get_data_dict(master_row, book_value_df, sic_mapping, lm_dictionary, ccmlinktable, market_df, PERMNO):
    financial_data = {
        'gvkey': None,
        'gvkey_unique': None,
        'LPERMNO': None,
        'LPERMNO_unique': None,
        'LPERMCO': None,
        'LPERMCO_unique': None,
        'ccmlinktable_com_names': None,
        'nasdaq_dummy': None, 
        'price_minus_one_day': None, 
        'volume_minus_one_day': None,
        'shares_outstanding_minus_one_day': None,
        'ff_industry': None,
        'RET_qeom': None, 
        'market_vwretd_qeom': None,
        'turnover': None,
        'book_value_per_share': None,
        'quater': int(master_row['fname'][3:4]),
        'year': int(master_row['fname'][5:9]),
    }
    financial_columns_count = len(financial_data.keys())
    _fill_financial_data(financial_data, master_row, book_value_df, sic_mapping, ccmlinktable, market_df, PERMNO)
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

    if financial_data['RET_qeom'] is not None:
        fname_path = os.path.join('parsed', str(financial_data['year']), master_row['fname'])
        textual_columns_count = len(textual_data.keys())
        _fill_textual_data(textual_data, fname_path, lm_dictionary)
        assert len(textual_data.keys()) == textual_columns_count

    data = {}
    data.update(financial_data)
    data.update(textual_data)
    return data


def _fill_textual_data(row, fname, lm_dictionary):
    if not os.path.isfile(fname):
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
            if lm_dictionary[token].negative:
                row['percent_negative'] += 1
                # print(token)
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


def _fill_financial_data(data, master_row, book_value_df, sic_mapping, ccmlinktable, market_df, PERMNO):
    permno_match = ccmlinktable[
        (ccmlinktable['LINKDT'] <= master_row['filingdate']) 
        & (ccmlinktable['LINKENDDT'] >= master_row['filingdate']) 
        & (ccmlinktable['cik'] == master_row['cik'])
    ]
    if permno_match.empty:
        # No permno match
        return

    data['gvkey'] = permno_match['gvkey'].value_counts().idxmax()
    data['gvkey_unique'] = len(permno_match['gvkey'].unique())

    data['LPERMNO'] = permno = permno_match['LPERMNO'].value_counts().idxmax()
    data['LPERMNO_unique'] = len(permno_match['LPERMNO'].unique())

    data['LPERMCO'] = permno_match['LPERMCO'].value_counts().idxmax()
    data['LPERMCO_unique'] = len(permno_match['LPERMCO'].unique())

    # This is for debugging
    data['ccmlinktable_com_names'] = ';'.join(set(name.upper() for name in permno_match['conm']))

    if not permno or not perm_number_table_exists(PERMNO, permno):
        # No stock data at all
        return

    df = pd.read_sql("select * from '%s'" % permno, PERMNO, index_col='rowid')
    # If ‘coerce’, then invalid parsing will be set as NaN
    df['RET'] = pd.to_numeric(df['RET'], errors='coerce')
    df['VOL'] = pd.to_numeric(df['VOL'], errors='coerce')
    df['PRC'] = pd.to_numeric(df['PRC'], errors='coerce')
    df['SHROUT'] = pd.to_numeric(df['SHROUT'], errors='coerce')

    #  If the closing price is not available on any given trading day, the number in the price field has a negative sign to indicate that it is a bid/ask average and not an actual closing price
    df['PRC'] = df['PRC'].abs()
    # df['PRC'].values[df['PRC'].values < 0] = np.nan

    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    sub_df = df.loc[df['date'] == master_row['filingdate']]

    if sub_df.empty:
        # No stock data on filing date
        return 

    # First row from the queried df
    row = sub_df.iloc[0]

    # Get the row number from original df based on index (row.name)
    idx = df.index.get_loc(row.name)

    # Use the row number to look for neighbour rows

    four_day_period = df.iloc[idx:idx+4]

    data['nasdaq_dummy'] = 1 if row['PRIMEXCH'] == 'Q' else 0
    data['price_minus_one_day'] = df.iloc[idx-1]['PRC']
    data['volume_minus_one_day'] = df.iloc[idx-1]['VOL']
    data['shares_outstanding_minus_one_day'] = df.iloc[idx-1]['SHROUT']
    data['ff_industry'] = sic_mapping.get(df.iloc[idx-1]['SICCD'])


    RET_four_day_period = four_day_period["RET"]
    RET_four_day_period += 1
    data['RET_qeom'] = stats.gmean(RET_four_day_period)

    # vwretd_four_day_period = four_day_period["vwretd"]
    # vwretd_four_day_period += 1
    # data['vwretd_qeom'] = stats.gmean(RET_four_day_period)

    max_date = four_day_period['date'].max()
    min_date = four_day_period['date'].min()
    market_four_day_period = market_df[(market_df['market_date'] <= max_date) & (market_df['market_date'] >= min_date)]

    vwretd_market_four_day_period = market_four_day_period['vwretd']
    vwretd_market_four_day_period += 1
    data['market_vwretd_qeom'] = stats.gmean(vwretd_market_four_day_period)



    history = df.iloc[idx - 252 : idx -6]
    FILING_DATE_SHROUT = df.iloc[idx]['SHROUT']
    # The volume of shares traded in days [−252,−6] prior to thefile date divided by shares outstanding on the file date. 
    # Atleast 60 observations of daily volume must be available to be included in the sample.
    if len(history) < 60 or not FILING_DATE_SHROUT:
        data['turnover'] = None
    else:
        data['turnover'] = history['VOL'].sum(axis=0) / FILING_DATE_SHROUT

    # Book-to-market COMPUSTAT data available
    company_values = book_value_df.loc[book_value_df['gvkey'] == data['gvkey']].loc[book_value_df['fyear'] == str(data['year'])]
    if company_values.empty:
        return

    row = company_values.iloc[0]
    data['book_value_per_share'] = row['bkvlps']


def test():
    lm_dictionary = load_masterdictionary(C.MASTER_DICT_PATH)
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
    fname = '/media/elmeri/T5-SSD/bachelor/parsed/2011/QTR1/20110228_10-K_edgar_data_73309_0001193125-11-049351_1.txt'
    _fill_textual_data(textual_data, fname, lm_dictionary)
    import pdb; pdb.set_trace()
    print(textual_data)


def main():
    with connect(C.MAIN_DB_NAME) as MAIN, connect(C.PERMNO_DB_NAME) as PERMNO:
        edit_master(MAIN, PERMNO)

if __name__ == '__main__':
    main()
    # test()
