
import csv
import pandas as pd
import glob
from sqlite3 import connect

import constants as C
from helpers import (
    download_masterindex,
    edgar_filename,
)


def master_to_db():
    path = 'data/*MASTER.csv' # use your path
    all_files = glob.glob(path)

    li = []

    for filename in all_files:
        print(filename)
        df = pd.read_csv(filename, index_col=None, header=0, sep=';')
        df.cik = df.cik.apply(lambda x: str(int(x)).zfill(10))
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    with connect(C.MAIN_DB_NAME) as conn:
        frame.to_sql(name='master', con=conn, if_exists='replace')


def master_idx_to_csv(year):
    COLUMNS = [
        'cik',
        'name',
        'form',
        'filingdate',
        'url',
        'fname',
    ]
    
    with open(C.PARM_PATH + "{}_MASTER.csv".format(year), 'w') as f_out:
        wr = csv.writer(f_out, lineterminator='\n', delimiter=';')
        wr.writerow(COLUMNS)

        for qtr in range(C.PARM_BGNQTR, C.PARM_ENDQTR + 1):
            if year == 2019 and qtr == 4:
                return
            file_count = {}
            path = 'QTR{0}/'.format(str(qtr))
            masterindex = download_masterindex(year, qtr, True)
            for record in masterindex:
                if record.form not in C.PARM_FORMS:
                    continue
                line = [
                    record.cik,
                    record.name,
                    record.form,
                    record.filingdate,
                    record.url,
                    edgar_filename(record, path, file_count)
                ]
                assert len(line) == len(COLUMNS)
                wr.writerow(line)


def main():
    for year in range(C.PARM_BGNYEAR, C.PARM_ENDYEAR + 1):
        master_idx_to_csv(year)

if __name__ == '__main__':
    main()
