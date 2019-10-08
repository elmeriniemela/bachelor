
import constants as C
import csv
from helpers import (
    download_masterindex,
    edgar_filename,
)


def master_idx_to_csv(year):
    OUTPUT_FIELDS = [
        'cik',
        'name',
        'form',
        'filingdate',
        'url',
        'fname',
    ]
    
    with open(C.PARM_PATH + "{}_MASTER.csv".format(year), 'w') as f_out:
        wr = csv.writer(f_out, lineterminator='\n', delimiter=';')
        wr.writerow(OUTPUT_FIELDS)

        for qtr in range(C.PARM_BGNQTR, C.PARM_ENDQTR + 1):
            if year == 2019 and qtr == 4:
                return
            file_count = {}
            path = 'QTR{0}/'.format(str(qtr))
            masterindex = download_masterindex(year, qtr, True)
            for record in masterindex:
                if record.form not in C.PARM_FORMS:
                    continue
                wr.writerow([
                    record.cik,
                    record.name,
                    record.form,
                    record.filingdate,
                    record.url,
                    record.url,
                    edgar_filename(record, path, file_count)
                ])


def main():
    for year in range(C.PARM_BGNYEAR, C.PARM_ENDYEAR + 1):
        master_idx_to_csv(year)

if __name__ == '__main__':
    main()
