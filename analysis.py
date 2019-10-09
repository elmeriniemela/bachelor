import pandas as pd
from sqlite3 import connect

with connect("bachelor.db") as conn:
    df = pd.read_sql(sql='select * from master', con=conn, index_col='index')
    df['filingdate'] = pd.to_datetime(df['filingdate'], format='%Y%m%d')
