
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

BAD_DOCUMENT_TYPES = {'GRAPHIC', 'ZIP', 'EXCEL', 'JSON', 'PDF', 'XML'}

FILE_STATS = """\
<FileStats>

    <OriginalChars>{original_chars}</OriginalChars>

    <CurrentChars>{current_chars}</CurrentChars>

    <PercentKept>{percent_kept}</PercentKept>

</FileStats>

"""
FAKE_LINE_SEPARATOR = ';;;;;;;;;;;;;;;;;'

GOOD_DOCUMENT_RE_LIST = [re.compile("<TYPE>{}</TYPE>".format(t), re.IGNORECASE) for t in C.PARM_FORMS]

def extract_text(dest_path, raw_data):
    # Close type tag
    only_text = re.sub(r"<TYPE>(\S+)", r"<TYPE>\1</TYPE>", raw_data)
    header = ''
    headermatch =  RE_SEC_HEADER.search(only_text)
    if headermatch:
        header = headermatch.group()
        only_text = only_text.replace(header, '')

    
    # Lets do regex on one line, to make things easier
    only_text = only_text.replace('\n', FAKE_LINE_SEPARATOR)

    # Remove all non 10-K documents like exhibitions xml files, json files, graphic files etc..
    all_documets = re.findall(r'<DOCUMENT[\w\W]*?</DOCUMENT>', only_text, re.IGNORECASE)
    kept_documents = [d for d in all_documets if any(RE.search(d) for RE in GOOD_DOCUMENT_RE_LIST)]


    only_text = '\n'.join(kept_documents)


    # Remove all XBRL – all characters between <XBRL …> … </XBRL> are deleted.
    only_text = re.sub(r"<XBRL[\w\W]*?</XBRL>", "", only_text)

    # Remove all tables
    only_text = re.sub(r"<TABLE[\w\W]*?</TABLE>", "", only_text)


    only_text = re.sub(r"-----BEGIN PRIVACY-ENHANCED MESSAGE-----", "", only_text)
    only_text = re.sub(r"-----END PRIVACY-ENHANCED MESSAGE-----", "", only_text)
    only_text = re.sub(r"<[\w\W]*?>", "", only_text)

    only_text = re.sub(r"&nbsp;", " ", only_text, re.IGNORECASE)
    only_text = re.sub(r"&#\d+;", " ", only_text, re.IGNORECASE)


    # Add back line separators
    only_text = only_text.replace(FAKE_LINE_SEPARATOR, '\n')

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


if __name__ == '__main__':
    main()
