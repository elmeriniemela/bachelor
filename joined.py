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

"""



all_stock_columns = [
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
) """ + ALL_STOCS_QUERY

def edit_master(conn):
    master = pd.read_sql("select * from master_joined", conn, index_col='index')
    master['lpermno'] = master['lpermno'].apply(lambda x: int(x))
    # master['filingdate'] = pd.to_datetime(master['filingdate'], format='%Y%m%d')
    master.to_sql(name='master_joined', con=conn, if_exists='replace')
    print(master)


def clean_all_stocks(conn):
    df_concat = read_all_stocks(conn)
    df_concat.to_sql(name='all_stocks_cleaned', con=conn, if_exists='replace')

def read_all_stocks(conn):
    all_chunks = []
    generator = pd.read_sql(ALL_STOCS_QUERY, conn, index_col='index', chunksize=1000000)
    for all_stock in generator:
        all_stock['date'] = pd.to_datetime(all_stock['date'], format='%Y%m%d')
        all_stock['PERMNO'] = all_stock['PERMNO'].apply(lambda x: int(x))
        all_chunks.append(all_stock)
    return pd.concat(all_chunks)

def read_filing_returns(conn, permno, filing_date):
    query = "select * from all_stocks_cleaned where PERMNO=%s and date >= '%s' LIMIT 4" % (
        permno, filing_date)
    print(query)
    return pd.read_sql(query, conn, index_col='index')

def read_master(conn):
    return pd.read_sql("select * from master_joined", conn, index_col='index')

def calculate_excess(row):

    related_rows = read_filing_returns(conn, row['lpermno'], row['filingdate'])
    import pdb; pdb.set_trace()

with connect("bachelor.db") as conn:
    # clean_all_stocks(conn)
    master = read_master(conn)
    master['excess_filing_returns_median'] = master.apply(calculate_excess, axis=1)
