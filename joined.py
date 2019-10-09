import pandas as pd
import glob
from sqlite3 import connect
import time
import datetime

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

SQL_SELECT = """

SELECT master.cik, ccm_lookup.lpermno, master.name, master.form, master.filingdate, master.url, master.fname
FROM master
INNER JOIN ccm_lookup ON ccm_lookup.cik=master.cik WHERE ccm_lookup.lpermno IS NOT NULL;

"""

SQL_create_all_stocks_primary_key = """
CREATE TABLE all_stocks_primary_key("index" INTEGER PRIMARY KEY AUTOINCREMENT, "PERMNO" TEXT, "date" TEXT, "NAMEENDT" TEXT, "SHRCD" TEXT, "EXCHCD" TEXT, "SICCD" TEXT, "NCUSIP" TEXT, "TICKER" TEXT, "COMNAM" TEXT, "SHRCLS" TEXT, "TSYMBOL" TEXT, "NAICS" TEXT, "PRIMEXCH" TEXT, "TRDSTAT" TEXT, "SECSTAT" TEXT, "PERMCO" TEXT, "ISSUNO" TEXT, "HEXCD" TEXT, "HSICCD" TEXT, "CUSIP" TEXT, "DCLRDT" TEXT, "DLAMT" TEXT, "DLPDT" TEXT, "DLSTCD" TEXT, "NEXTDT" TEXT, "PAYDT" TEXT, "RCRDDT" TEXT, "SHRFLG" TEXT, "HSICMG" TEXT, "HSICIG" TEXT, "DISTCD" TEXT, "DIVAMT" TEXT, "FACPR" TEXT, "FACSHR" TEXT, "ACPERM" TEXT, "ACCOMP" TEXT, "NWPERM" TEXT, "DLRETX" TEXT, "DLPRC" TEXT, "DLRET" TEXT, "TRTSCD" TEXT, "NMSIND" TEXT, "MMCNT" TEXT, "NSDINX" TEXT, "BIDLO" TEXT, "ASKHI" TEXT, "PRC" TEXT, "VOL" TEXT, "RET" TEXT, "BID" TEXT, "ASK" TEXT, "SHROUT" TEXT, "CFACPR" TEXT, "CFACSHR" TEXT, "OPENPRC" TEXT, "NUMTRD" TEXT, "RETX" TEXT, "vwretd" TEXT, "vwretx" TEXT, "ewretd" TEXT, "ewretx" TEXT, "sprtrn" TEXT )
INSERT INTO all_stocks_primary_key(PERMNO, date, NAMEENDT, SHRCD, EXCHCD, SICCD, NCUSIP, TICKER, COMNAM, SHRCLS, TSYMBOL, NAICS, PRIMEXCH, TRDSTAT, SECSTAT, PERMCO, ISSUNO, HEXCD, HSICCD, CUSIP, DCLRDT, DLAMT, DLPDT, DLSTCD, NEXTDT, PAYDT, RCRDDT, SHRFLG, HSICMG, HSICIG, DISTCD, DIVAMT, FACPR, FACSHR, ACPERM, ACCOMP, NWPERM, DLRETX, DLPRC, DLRET, TRTSCD, NMSIND, MMCNT, NSDINX, BIDLO, ASKHI, PRC, VOL, RET, BID, ASK, SHROUT, CFACPR, CFACSHR, OPENPRC, NUMTRD, RETX, vwretd, vwretx, ewretd, ewretx, sprtrn) SELECT * FROM all_stocks;

"""

SQL_INDEX = """

CREATE INDEX filing_date_returns_idx 
ON all_stocks_cleaned(PERMNO, date); 

CREATE INDEX permno_idx 
ON all_stocks(PERMNO); 

"""



all_stock_columns = [
    'index',
    'date',
    'PERMNO',
    'PRC',
    'VOL',
    'SHROUT',
    'ewretd',
    'ewretx',
]

ALL_STOCS_QUERY = "SELECT %s FROM all_stocks_primary_key" % ', '.join('"{}"'.format(s) for s in all_stock_columns)

SQL_CREATE_CLEANED = """

CREATE TABLE IF NOT EXISTS "all_stocks_cleaned" (
"index" INTEGER,
  "date" TIMESTAMP,
  "PERMNO" INTEGER,
  "PRC" TEXT,
  "VOL" TEXT,
  "SHROUT" TEXT,
  "ewretd" TEXT,
  "ewretx" TEXT
);
CREATE INDEX "ix_all_stocks_cleaned_index"ON "all_stocks_cleaned" ("index");

INSERT INTO all_stocks_cleaned(
    'date', 
    'PERMNO',
    'PRC',
    'VOL',
    'SHROUT',
    'ewretd',
    'ewretx'
) SELECT "date", "PERMNO", "PRC", "VOL", "SHROUT", "ewretd", "ewretx" FROM all_stocks_primary_key"""

def edit_master(MAIN):
    master = pd.read_sql("select * from master_joined", MAIN, index_col='index')
    master['lpermno'] = master['lpermno'].apply(lambda x: int(x))
    # master['filingdate'] = pd.to_datetime(master['filingdate'], format='%Y%m%d')
    master.to_sql(name='master_joined', con=MAIN, if_exists='replace')
    print(master)


def clean_all_stocks(MAIN):
    df_concat = read_all_stocks(MAIN)
    df_concat.to_sql(name='all_stocks_cleaned', con=MAIN, if_exists='replace')

def read_all_stocks(MAIN):
    all_chunks = []
    generator = pd.read_sql(ALL_STOCS_QUERY, MAIN, index_col='index', chunksize=1000000)
    for all_stock in generator:
        all_stock['date'] = pd.to_datetime(all_stock['date'], format='%Y%m%d')
        all_stock['PERMNO'] = all_stock['PERMNO'].apply(lambda x: int(x))
        all_chunks.append(all_stock)
    return pd.concat(all_chunks)

def read_filing_returns(master_row, MAIN, PERMNO, n_rows):
    print("Processing row %s/%s" % (master_row.name, n_rows))
    permno = master_row['lpermno']
    filing_date = master_row['filingdate']
    columns = [
        'price_minus_one_day', 
        'median_ewretd', 
        'sixty_days_trading'
    ]
    if not perm_number_table_exists(PERMNO, permno):
        return pd.Series([None, None, False], index=columns)

    query = "select * from '%s'" % permno
    df = pd.read_sql(query, PERMNO, index_col='rowid')
    df['date'] = pd.to_datetime(df.date)
    df.sort_values(by=['date'])
    sub_df = df.loc[df['date'] == filing_date]
    if len(sub_df) == 0:
        return pd.Series([None, None, False], index=columns)
    assert len(sub_df) == 1
    row = sub_df.iloc[0]
    idx = df.index.get_loc(row.name)
    history = df.iloc[idx - 60 : idx + 60]
    sixty_days_trading = len(history) == 120
    prc = df.iloc[idx-1]['PRC']
    price_minus_one_day = float(prc) if prc else None
    median_ewretd = df.iloc[idx:idx+4]['ewretd'].median(axis=0)

    vals = [
        price_minus_one_day, 
        median_ewretd, 
        sixty_days_trading,
    ]
    return pd.Series(vals, index=columns)

def read_master(MAIN):
    return pd.read_sql("select * from master_joined", MAIN, index_col='index')


def create_company_tables(MAIN, PERMNO):
    cur = MAIN.cursor()
    res = cur.execute("SELECT DISTINCT PERMNO from all_stocks").fetchall()
    perm_numbers = set(t[0] for t in res)
    print("Unique PERMNO's: ", len(perm_numbers))
    for perm_no in perm_numbers:
        create_based_on_permno(MAIN, PERMNO, perm_no)


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


def add_excess_to_master(MAIN, PERMNO):
    master = read_master(MAIN)
    filings = master.apply(lambda row: read_filing_returns(row, MAIN, PERMNO, len(master)), axis=1)
    joined = master.join(filings)
    joined.to_sql(name='master_filing_returns', con=MAIN, if_exists='replace')


def describe(CONN):
    cursor = CONN.cursor()
    tablesToIgnore = ["sqlite_sequence"]
    totalTables = 0
    totalColumns = 0
    totalRows = 0
    totalCells = 0
    
    # Get List of Tables:      
    tableListQuery = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
    cursor.execute(tableListQuery)
    tables = map(lambda t: t[0], cursor.fetchall())
    
    for table in tables:
    
        if (table in tablesToIgnore):
            continue            
            
        columnsQuery = "PRAGMA table_info(%s)" % table
        cursor.execute(columnsQuery)
        numberOfColumns = len(cursor.fetchall())
        
        rowsQuery = "SELECT Count() FROM '%s'" % table
        cursor.execute(rowsQuery)
        numberOfRows = cursor.fetchone()[0]
        
        numberOfCells = numberOfColumns*numberOfRows
        
        print("%s\t%d\t%d\t%d" % (table, numberOfColumns, numberOfRows, numberOfCells))
        
        totalTables += 1
        totalColumns += numberOfColumns
        totalRows += numberOfRows
        totalCells += numberOfCells

    print( "" )
    print( "Number of Tables:\t%d" % totalTables )
    print( "Total Number of Columns:\t%d" % totalColumns )
    print( "Total Number of Rows:\t%d" % totalRows )
    print( "Total Number of Cells:\t%d" % totalCells )


def main():
    with connect("MAIN.db") as MAIN, connect("PERMNO.db") as PERMNO:
        # create_company_tables(MAIN, PERMNO)
        # describe(PERMNO)
        add_excess_to_master(MAIN, PERMNO)

if __name__ == '__main__':
    main()