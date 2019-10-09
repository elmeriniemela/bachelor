import pandas as pd
import glob
from sqlite3 import connect

path = 'data/*MASTER.csv' # use your path
all_files = glob.glob(path)

li = []

for filename in all_files:
    print(filename)
    df = pd.read_csv(filename, index_col=None, header=0, sep=';')
    df.cik = df.cik.apply(lambda x: str(int(x)).zfill(10))
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

with connect("bachelor.db") as conn:
    frame.to_sql(name='master', con=conn, if_exists='replace')