import pandas as pd
import glob
from sqlite3 import connect


SQL_SELECT = """

SELECT master.cik, ccm_lookup.lpermno, master.name, master.form, master.filingdate, master.url, master.fname
FROM master
INNER JOIN ccm_lookup ON ccm_lookup.cik=master.cik WHERE ccm_lookup.lpermno IS NOT NULL;

"""


with connect("bachelor.db") as conn:
    df = pd.read_sql(SQL_SELECT, conn)
    print(df)