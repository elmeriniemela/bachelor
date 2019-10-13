
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


def load_masterdictionary(file_path, print_flag=False, f_log=None, get_other=False):
    _master_dictionary = {}
    _sentiment_categories = ['negative', 'positive', 'uncertainty', 'litigious', 'constraining',
                             'strong_modal', 'weak_modal']
    # Load slightly modified nltk stopwords.  I do not use nltk import to avoid versioning errors.
    # Dropped from nltk: A, I, S, T, DON, WILL, AGAINST
    # Added: AMONG,
    _stopwords = ['ME', 'MY', 'MYSELF', 'WE', 'OUR', 'OURS', 'OURSELVES', 'YOU', 'YOUR', 'YOURS',
                       'YOURSELF', 'YOURSELVES', 'HE', 'HIM', 'HIS', 'HIMSELF', 'SHE', 'HER', 'HERS', 'HERSELF',
                       'IT', 'ITS', 'ITSELF', 'THEY', 'THEM', 'THEIR', 'THEIRS', 'THEMSELVES', 'WHAT', 'WHICH',
                       'WHO', 'WHOM', 'THIS', 'THAT', 'THESE', 'THOSE', 'AM', 'IS', 'ARE', 'WAS', 'WERE', 'BE',
                       'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'HAVING', 'DO', 'DOES', 'DID', 'DOING', 'AN',
                       'THE', 'AND', 'BUT', 'IF', 'OR', 'BECAUSE', 'AS', 'UNTIL', 'WHILE', 'OF', 'AT', 'BY',
                       'FOR', 'WITH', 'ABOUT', 'BETWEEN', 'INTO', 'THROUGH', 'DURING', 'BEFORE',
                       'AFTER', 'ABOVE', 'BELOW', 'TO', 'FROM', 'UP', 'DOWN', 'IN', 'OUT', 'ON', 'OFF', 'OVER',
                       'UNDER', 'AGAIN', 'FURTHER', 'THEN', 'ONCE', 'HERE', 'THERE', 'WHEN', 'WHERE', 'WHY',
                       'HOW', 'ALL', 'ANY', 'BOTH', 'EACH', 'FEW', 'MORE', 'MOST', 'OTHER', 'SOME', 'SUCH',
                       'NO', 'NOR', 'NOT', 'ONLY', 'OWN', 'SAME', 'SO', 'THAN', 'TOO', 'VERY', 'CAN',
                       'JUST', 'SHOULD', 'NOW']

    with open(file_path) as f:
        _total_documents = 0
        _md_header = f.readline()
        for line in f:
            cols = line.split(',')
            _master_dictionary[cols[0]] = MasterDictionary(cols, _stopwords)
            _total_documents += _master_dictionary[cols[0]].doc_count
            if len(_master_dictionary) % 5000 == 0 and print_flag:
                print('\r ...Loading Master Dictionary' + ' {}'.format(len(_master_dictionary)), end='', flush=True)

    if print_flag:
        print('\r', end='')  # clear line
        print('\nMaster Dictionary loaded from file: \n  ' + file_path)
        print('  {0:,} words loaded in master_dictionary.'.format(len(_master_dictionary)) + '\n')

    if f_log:
        try:
            f_log.write('\n\n  load_masterdictionary log:')
            f_log.write('\n    Master Dictionary loaded from file: \n       ' + file_path)
            f_log.write('\n    {0:,} words loaded in master_dictionary.\n'.format(len(_master_dictionary)))
        except Exception as e:
            print('Log file in load_masterdictionary is not available for writing')
            print('Error = {0}'.format(e))

    if get_other:
        return _master_dictionary, _md_header, _sentiment_categories, _stopwords, _total_documents
    else:
        return _master_dictionary


def create_sentimentdictionaries(_master_dictionary, _sentiment_categories):

    _sentiment_dictionary = {}
    for category in _sentiment_categories:
        _sentiment_dictionary[category] = {}
    # Create dictionary of sentiment dictionaries with count set = 0
    for word in _master_dictionary.keys():
        for category in _sentiment_categories:
            if _master_dictionary[word].sentiment[category]:
                _sentiment_dictionary[category][word] = 0

    return _sentiment_dictionary


class MasterDictionary:
    def __init__(self, cols, _stopwords):
        self.word = cols[0].upper()
        self.sequence_number = int(cols[1])
        self.word_count = int(cols[2])
        self.word_proportion = float(cols[3])
        self.average_proportion = float(cols[4])
        self.std_dev_prop = float(cols[5])
        self.doc_count = int(cols[6])
        self.negative = int(cols[7])
        self.positive = int(cols[8])
        self.uncertainty = int(cols[9])
        self.litigious = int(cols[10])
        self.constraining = int(cols[11])
        self.superfluous = int(cols[12])
        self.interesting = int(cols[13])
        self.modal_number = int(cols[14])
        self.strong_modal = False
        if int(cols[14]) == 1:
            self.strong_modal = True
        self.moderate_modal = False
        if int(cols[14]) == 2:
            self.moderate_modal = True
        self.weak_modal = False
        if int(cols[14]) == 3:
            self.weak_modal = True
        self.sentiment = {}
        self.sentiment['negative'] = bool(self.negative)
        self.sentiment['positive'] = bool(self.positive)
        self.sentiment['uncertainty'] = bool(self.uncertainty)
        self.sentiment['litigious'] = bool(self.litigious)
        self.sentiment['constraining'] = bool(self.constraining)
        self.sentiment['strong_modal'] = bool(self.strong_modal)
        self.sentiment['weak_modal'] = bool(self.weak_modal)
        self.irregular_verb = int(cols[15])
        self.harvard_iv = int(cols[16])
        self.syllables = int(cols[17])
        self.source = cols[18]

        if self.word in _stopwords:
            self.stopword = True
        else:
            self.stopword = False
        return

if __name__ == '__main__':
    # Full test program in /TextualAnalysis/TestPrograms/Test_Load_MasterDictionary.py
    print(time.strftime('%c') + '\n')
    md = ('LoughranMcDonald_MasterDictionary_2018.csv')
    master_dictionary, md_header, sentiment_categories, stopwords, total_documents = load_masterdictionary(md, True, False, True)
    
    summary = dict(
        negative=0,
        positive=0,
        uncertainty=0,
        litigious=0,
        strong_modal=0,
        weak_modal=0,
        constraining=0,
    )
    for word, obj in master_dictionary.items():
        for key in summary:
            summary[key] += int(bool(getattr(obj, key)))
    
    print(summary)
    print('\n' + 'Normal termination.')
    print(time.strftime('%c') + '\n')
