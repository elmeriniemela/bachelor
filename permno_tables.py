
import pandas as pd
from sqlite3 import connect

import constants as C


def create_company_tables(ALL_STOCKS, PERMNO):
    all_stocks_cur = ALL_STOCKS.cursor()
    print("Creating index for PERMNO to make future queries faster.")
    all_stocks_cur.execute("CREATE INDEX IF NOT EXISTS permno_idx ON all_stocks(PERMNO)")
    print("Query for unique PERMNO's")
    res = all_stocks_cur.execute("SELECT DISTINCT PERMNO from all_stocks").fetchall()
    perm_numbers = set(t[0] for t in res)
    print("Unique PERMNO's: ", len(perm_numbers))
    perm_cur = PERMNO.cursor()
    for perm_no in perm_numbers:
        create_based_on_permno(ALL_STOCKS, PERMNO, perm_no)


def perm_number_table_exists(PERMNO, perm_no):
    cur = PERMNO.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % perm_no)
    return bool(res.fetchall())

def create_based_on_permno(ALL_STOCKS, PERMNO, perm_no):
    if perm_number_table_exists(PERMNO, perm_no):
        print("Table exists ", perm_no)
        return 
    print("Create table for ", perm_no)
    df = pd.read_sql("select rowid, * from all_stocks where PERMNO='%s'" % perm_no, ALL_STOCKS, index_col='rowid')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

    df = df.drop('PERMNO', axis=1)
    df.to_sql(name=perm_no, con=PERMNO, if_exists='fail')


def init_perno():
    with connect(C.ALL_STOCKS_DB_NAME) as ALL_STOCKS, connect(C.PERMNO_DB_NAME) as PERMNO:
        create_company_tables(ALL_STOCKS, PERMNO)



if __name__ == '__main__':
    init_perno()
