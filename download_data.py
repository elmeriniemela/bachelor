#!/usr/bin/pytho
"""
    Program to download EDGAR files by form type
    ND-SRAF / McDonald : 201606
    https://sraf.nd.edu
    Dependencies (i.e., modules you must already have downloaded)
      EDGAR_Forms.py
      EDGAR_Pac.py
      General_Utilities.py
"""

import time
import multiprocessing
import zipfile
from helpers import (
    quittable,
    download_masterindex,
    edgar_filename,
    download_to_zip,
)

import constants as C

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * +

#  NOTES
#        The EDGAR archive contains millions of forms.
#        For details on accessing the EDGAR servers see:
#          https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm
#
#        For large downloads you will sometimes get a hiccup in the server
#            and the file request will fail.  These errs are documented in
#            the log file.  You can manually download those files that fail.
#            Although I attempt to work around server errors, if the SEC's server
#            is sufficiently busy, you might have to try another day.
#
#       For a list of form types and counts by year:
#         "All SEC EDGAR Filings by Type and Year"
#          at https://sraf.nd.edu/textual-analysis/resources/#All%20SEC%20EDGAR%20Filings%20by%20Type%20and%20Year


#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * +


def download_forms(year):
    zip_fname = C.PARM_PATH + '{}.zip'.format(year)
    with zipfile.ZipFile(zip_fname, mode='a', compression=zipfile.ZIP_DEFLATED) as year_zip:
        initial_files = set(year_zip.namelist())
    
    print("{} files already downloaded at {}".format(len(initial_files), zip_fname))
    for qtr in range(C.PARM_BGNQTR, C.PARM_ENDQTR + 1):
        if year == 2019 and qtr == 4:
            return
        startloop = time.time()
        n_qtr = 0
        file_count = {}
        # Setup output path
        path = 'QTR{0}/'.format(str(qtr))
        masterindex = download_masterindex(year, qtr, True)
        if masterindex:
            for item in masterindex:
                if item.form not in C.PARM_FORMS:
                    continue
                
                fname = edgar_filename(item, path, file_count)
                
                if fname in initial_files:
                    # print('File already exists: {0}'.format(fname))
                    continue
                initial_files.add(fname)
                if n_qtr % 10 == 0:
                    process_index = multiprocessing.current_process().name
                    print('... Loading files {}:{} (process: {}, time: {}, download count: {}, total count: {})'.format(
                        year, qtr, process_index, time.strftime("%H:%M:%S"), n_qtr, len(initial_files)))

                n_qtr += 1
                # Setup EDGAR URL and output file name
                url = C.PARM_EDGARPREFIX + item.url
                return_url = download_to_zip(url, fname, zip_fname, C.PARM_LOGFILE)
                if return_url:
                    print("Failed to download: ", url)
        print() # newline
        print(str(year) + ':' + str(qtr) + ' -> {0:,}'.format(n_qtr) + ' downloads completed.  Time = ' +
            time.strftime('%H:%M:%S', time.gmtime(time.time() - startloop)) +
            ' | ' + time.strftime('%c'))
        

def try_download(year):
    with quittable():
        download_forms(year)



def main():
    start = time.time()
    print('\n' + time.strftime('%c') + '\nND_SRAF:  Program EDGAR_DownloadForms.py\n')
    print("Downloading {}-{}: {}".format(C.PARM_BGNYEAR, C.PARM_ENDYEAR, C.PARM_FORMS))
    p = multiprocessing.Pool(8)
    try:
        p.map(try_download, C.YEARS_LIST)
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        p.terminate()
        p.join()

    else:
        print("Quitting normally")
        p.close()
        p.join()

    print('\nEDGAR_DownloadForms.py | Normal termination | ' +
          time.strftime('%H:%M:%S', time.gmtime(time.time() - start)))
    print(time.strftime('%c'))






if __name__ == '__main__':
    main()
    