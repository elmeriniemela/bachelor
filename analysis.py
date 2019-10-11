import pandas as pd
import glob
from sqlite3 import connect
import time
import datetime
from pprint import pprint

import constants as C

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
    joined = master.join(edited_master)
    if len(joined.index) != len(master.index):
        import pdb; pdb.set_trace()
    joined.to_sql(name='master_edited', con=MAIN, if_exists='replace')


def edit_market(MAIN):
    market = pd.read_sql("select rowid, * from market_index", MAIN, index_col='rowid')
    market['DATE'] = pd.to_datetime(market['DATE'], format='%Y%m%d')
    market.to_sql(name='market_index', con=MAIN, if_exists='replace')



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
    df.sort_values(by=['date'])
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
    


def main():
    with connect(C.MAIN_DB_NAME) as MAIN, connect(C.PERMNO_DB_NAME) as PERMNO:
        create_company_tables(MAIN, PERMNO)
        edit_master(MAIN, PERMNO)

if __name__ == '__main__':
    main()
