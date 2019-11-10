
from bs4 import BeautifulSoup
from lxml import etree
import re
import os
import zipfile
import time
import multiprocessing
from collections import defaultdict

import constants as C
from helpers import quittable

RE_SEC_HEADER = re.compile(r"<(IMS-HEADER|SEC-HEADER)>[\w\W]*?</(IMS-HEADER|SEC-HEADER)>", re.MULTILINE)

FILE_STATS = """\
<FileStats>

    <OriginalChars>{original_chars}</OriginalChars>

    <CurrentChars>{current_chars}</CurrentChars>

    <PercentKept>{percent_kept}</PercentKept>

</FileStats>

"""

GOOD_DOCUMENT_RE_LIST = [re.compile("<TYPE>{}</TYPE>".format(t), flags=re.IGNORECASE) for t in C.PARM_FORMS]

RE_DOCUMENT = re.compile(r'<DOCUMENT[ >][\w\W]*?</DOCUMENT>', flags=re.IGNORECASE | re.MULTILINE)

RE_XBRL = re.compile(r'<XBRL[ >][\w\W]*?</XBRL>', flags=re.IGNORECASE | re.MULTILINE)

RE_TABLE = re.compile(r'<TABLE[ >][\w\W]*?</TABLE>', flags=re.IGNORECASE | re.MULTILINE)

RE_MARKUP = re.compile(r'<[\w\W]*?>', flags=re.IGNORECASE | re.MULTILINE)

RE_PRIVACY_START = re.compile(r'-----BEGIN PRIVACY-ENHANCED MESSAGE-----', flags=re.IGNORECASE)

RE_PRIVACY_END = re.compile(r'-----END PRIVACY-ENHANCED MESSAGE-----', flags=re.IGNORECASE)


RE_EXCESS_WHITESPACE = re.compile(r'\s{3,}')

RE_PDF = re.compile(r'<FILENAME>.*?\.pdf')

BAD_DOCUMENT_RE_LIST = [RE_PDF]


def extract_text(dest_path, raw_data):
    # Close type tag
    only_text = re.sub(r"<TYPE>(\S+)", r"<TYPE>\1</TYPE>", raw_data)

    # Save SEC header
    header = ''
    headermatch =  RE_SEC_HEADER.search(only_text)
    if headermatch:
        header = headermatch.group()
        only_text = only_text.replace(header, '')

    
    # Remove all non 10-K documents like exhibitions xml files, json files, graphic files etc..
    all_documets = RE_DOCUMENT.findall(only_text)
    kept_documents = [d for d in all_documets if any(RE.search(d) for RE in GOOD_DOCUMENT_RE_LIST)]
    kept_documents = [d for d in kept_documents if not any(RE.search(d) for RE in BAD_DOCUMENT_RE_LIST)]


    only_text = '\n'.join(kept_documents)

    # Remove all XBRL – all characters between <XBRL …> … </XBRL> are deleted.
    only_text = RE_XBRL.sub(" ", only_text)

    # Remove all tables
    only_text = RE_TABLE.sub(" ", only_text)

    only_text = RE_PRIVACY_START.sub(" ", only_text)
    only_text = RE_PRIVACY_END.sub(" ", only_text)

    # Remove all html tags
    only_text = RE_MARKUP.sub(" ", only_text)

    only_text = RE_EXCESS_WHITESPACE.sub(" ", only_text)

    # Remove all html entities
    only_text = BeautifulSoup(only_text, 'lxml').get_text(' ')

    # Remove non ascii chars
    only_text = ''.join(i if ord(i) < 128 else ' ' for i in only_text)

    original_chars = len(raw_data)
    current_chars = len(only_text)
    percent_kept = (current_chars / original_chars) * 100
    process_index = multiprocessing.current_process().name
    print("{:.2f} % and {}/{} documents kept. ({}) {}".format(percent_kept, len(kept_documents), len(all_documets), process_index, dest_path))

    with open(dest_path, 'w') as f:
        f.write(FILE_STATS.format(
            original_chars=original_chars,
            current_chars=current_chars,
            percent_kept=percent_kept,
        ))
        f.write(header)
        f.write('<DOCUMENT>\n' + only_text +'\n</DOCUMENT>')


def parsed_file_path(zip_path, year):
    file_path = os.path.join('parsed', year, os.path.normpath(zip_path))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


def create_file_data_que():
    que = []
    for zip_file_path in C.FILE_LIST:
        with zipfile.ZipFile(zip_file_path, mode='r') as zip_f_obj:
            year = zip_file_path[5:-4]
            for src_path in zip_f_obj.namelist():
                dest_path = parsed_file_path(src_path, year)
                if os.path.exists(dest_path):
                    print("File exists: {}".format(dest_path))
                    continue
                que.append((zip_file_path, dest_path, src_path))
    return que


def try_clean(args):
    zip_file_path, dest_path, src_path = args
    with quittable():
        with zipfile.ZipFile(zip_file_path, mode='r') as zip_f_obj:
            with zip_f_obj.open(src_path, 'r') as f:
                try:
                    data = f.read().decode(errors='ignore')
                except Exception as error:
                    print(error)
                    return
        extract_text(dest_path, data)

def main():

    start = time.time()
    print('\n' + time.strftime('%c') + '\nND_SRAF:  Program clean_data.py\n')
    print("Extracting text from {} zip files.".format(len(C.FILE_LIST)))

    que = create_file_data_que()
    print("{} files in que.".format(len(que)))
    multiprocess_que(que)

    print('\nclean_data.py | Normal termination | ' +
          time.strftime('%H:%M:%S', time.gmtime(time.time() - start)))
    print(time.strftime('%c'))


def normal_process_que(que):
    for args in que:
        try_clean(args)

def multiprocess_que(que):
    n_process = multiprocessing.cpu_count()
    print("Using {} processes".format(n_process))
    p = multiprocessing.Pool(n_process)
    try:
        p.map(try_clean, que)
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        p.terminate()
        p.join()

    else:
        print("Quitting normally")
        p.close()
        p.join()



def test():

    def parse_one_file(fname):
        year = fname[5:9]
        data_zip = f'/media/elmeri/T5-SSD/bachelor/data/{year}.zip'
        with zipfile.ZipFile(data_zip, mode='r') as _zipfile:
            _zipfile.extract(fname, '/tmp')
        with open('/tmp/' + fname, 'rb') as f_obj:
            data = f_obj.read().decode(errors='ignore')
        
        extract_text(
            '/tmp/test.txt',
            data
        )



    # parse_one_file('QTR1/20080222_10-K_edgar_data_1000229_0001000229-08-000005_1.txt')

    # parse_one_file('QTR1/20110228_10-K_edgar_data_73309_0001193125-11-049351_1.txt')
    parse_one_file('QTR4/19961206_10-K-A_edgar_data_846876_0000891554-96-000905_1.txt')

if __name__ == '__main__':
    # main()
    test()
