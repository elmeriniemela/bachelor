
from contextlib import contextmanager
import requests
import zipfile
import time
import io

@contextmanager
def quittable():
    try:
        yield
    except (KeyboardInterrupt):
        process_index = multiprocessing.current_process().name
        print("{} quitting gracefully.".format(process_index))

def download_masterindex(year, qtr, flag=False):
    # Download Master.idx from EDGAR
    # Loop accounts for temporary server/ISP issues
    # ND-SRAF / McDonald : 201606


    number_of_tries = 10
    sleep_time = 10  # Note sleep time accumulates according to err


    PARM_ROOT_PATH = 'https://www.sec.gov/Archives/edgar/full-index/'

    start = time.time()  # Note: using clock time not CPU
    masterindex = []
    #  using the zip file is a little more complicated but orders of magnitude faster
    append_path = str(year) + '/QTR' + str(qtr) + '/master.zip'  # /master.idx => nonzip version
    sec_url = PARM_ROOT_PATH + append_path

    for i in range(1, number_of_tries + 1):
        try:
            r = requests.get(sec_url)
            zip_obj = zipfile.ZipFile(io.BytesIO(r.content))
            records = zip_obj.open('master.idx').read().decode('utf-8', 'ignore').splitlines()[10:]
            break
        except Exception as exc:
            if i == 1:
                print('\nError in download_masterindex')
            print('  {0}. _url:  {1}'.format(i, sec_url))

            print('  Warning: {0}  [{1}]'.format(str(exc), time.strftime('%c')))
            if '404' in str(exc):
                break
            if i == number_of_tries:
                return False
            print('     Retry in {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
            sleep_time += sleep_time


    # Load m.i. records into masterindex list
    for line in records:
        mir = MasterIndexRecord(line)
        if not mir.err:
            masterindex.append(mir)

    if flag:
        print('download_masterindex:  ' + str(year) + ':' + str(qtr) + ' | ' +
              'len() = {:,}'.format(len(masterindex)) + ' | Time = {0:.4f}'.format(time.time() - start) +
              ' seconds')

    return masterindex


class MasterIndexRecord:
    def __init__(self, line):
        self.err = False
        parts = line.split('|')
        if len(parts) == 5:
            self.cik = int(parts[0])
            self.name = parts[1]
            self.form = parts[2]
            self.filingdate = int(parts[3].replace('-', ''))
            self.url = parts[4]
        else:
            print("INCORRECT LINE: ", line)
            self.err = True
        return


def edgar_filename(item, path, file_count):
    fid = str(item.cik) + str(item.filingdate) + item.form
    # Keep track of filings and identify duplicates
    if fid in file_count:
        file_count[fid] += 1
    else:
        file_count[fid] = 1
    fname = (path + str(item.filingdate) + '_' + item.form.replace('/', '-') + '_' +
                item.url.replace('/', '_'))
    fname = fname.replace('.txt', '_' + str(file_count[fid]) + '.txt')
    return fname





def download_to_zip(_url, _fname, _zip_fname, logging_fname=None):
    # download file from 'url' and write to '_fname'
    # Loop accounts for temporary server/ISP issues

    number_of_tries = 3
    sleep_time = 10  # Note sleep time accumulates according to err

    for i in range(1, number_of_tries + 1):
        # 3 minutes timeout, incase of network interrupts
        try:
            r = requests.get(_url)
            data = r.content
        except Exception as exc:
            if i == 1:
                print('\n==>urlopen error in download_to_zip.py')
            print('  {0}. _url:  {1}'.format(i, _url))
            print('     _fname:  {0}'.format(_fname))
            print('     Warning: {0}  [{1}]'.format(str(exc), time.strftime('%c')))
            if '404' in str(exc):
                break
            print('     Retry in {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
            sleep_time += sleep_time
        else:
            # _zipfile.write(_fname, zipfile.ZIP_DEFLATED)
            # https://bugs.python.org/issue36434
            # https://github.com/python/cpython/pull/12559/commits
            # https://github.com/python/cpython/pull/12628/commits
            # USE PYTHON 3.7
            with zipfile.ZipFile(_zip_fname, mode='a', compression=zipfile.ZIP_DEFLATED) as _zipfile:
                with _zipfile.open(_fname, 'w') as f:
                    f.write(data)
            return

    print('\n  ERROR:  Download failed for')
    print('          url:  {0}'.format(_url))
    print('          _fname:  {0}'.format(_fname))
    if logging_fname:
        with open(logging_fname, 'a') as logger:
            logger.write('ERROR:  Download failed=>')
            logger.write('  _url: {0:75}'.format(_url))
            logger.write('  |  _fname: {0}'.format(_fname))
            logger.write('  |  {0}\n'.format(time.strftime('%c')))

    return True