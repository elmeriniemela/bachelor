


import zipfile
import csv
import os

import constants as C

all_files = 0

for fname in C.FILE_LIST:
    with zipfile.ZipFile(fname, mode='r') as _zipfile:
        year = fname[5:-4]
        master_count = 0
        master_path = C.PARM_PATH + "{}_MASTER.csv".format(year)
        if os.path.exists(master_path):
            with open(master_path, 'r') as f_out:
                wr = csv.reader(f_out, lineterminator='\n', delimiter=';')
                next(wr, None)  # skip the headers
                for line in wr:
                    master_count += 1

        file_count = len(set(_zipfile.namelist()))
        print("{} contains {}/{} files.".format(fname, file_count, master_count))
        all_files += file_count

print("Total filecount: {}".format(all_files))
