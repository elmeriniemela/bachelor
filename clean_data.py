
from bs4 import BeautifulSoup
from lxml import etree
import re
import os
import zipfile
import time
import multiprocessing
from selectolax.parser import HTMLParser
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


def parsed_file_path(zip_path, year):
    file_path = os.path.join('parsed2', year, os.path.normpath(zip_path))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


def get_text_selectolax(html):
    tree = HTMLParser(html)

    res = defaultdict(int)

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        res[tag.tag] += 1
        tag.decompose()
    for tag in tree.css('style'):
        res[tag.tag] += 1
        tag.decompose()

    for document in tree.css('document'):
        res[document.tag] += 1
        # Remove ASCII-Encoded segments – All document segment <TYPE> tags of GRAPHIC, ZIP, EXCEL, JSON, XML and PDF are deleted from the file.
        doc_type = document.css('type')
        if not doc_type:
            continue
        doc_type = doc_type[0].text()
        res[doc_type] += 1
        # Remove ASCII-Encoded segments – All document segment <TYPE> tags of GRAPHIC, ZIP, EXCEL, JSON, XML and PDF are deleted from the file.
        if doc_type in BAD_DOCUMENT_TYPES:
            document.decompose()
            continue
        
        # Remove all exhibitions 
        # For example, post–Sarbanes-Oxley, most 10-Ks contain Exhibit 31.1, 
        # pertainingto the certification of the 10-K by the CEO. 
        # The standard exhibit includes anumber of negative words, 
        # for example,untrue,omit,weaknesses,andfraud.
        if doc_type.startswith('EX-'):
            document.decompose()
            continue

    return tree.body.text(separator=' '), dict(res)


def extract_text(dest_path, raw_data):
    # Close type tag
    only_text = re.sub(r"<TYPE>(\S+)", r"<TYPE>\1</TYPE>", raw_data)

    # Remove all XBRL – all characters between <XBRL …> … </XBRL> are deleted.
    only_text = re.sub(r"<XBRL>.*?</XBRL>", "", only_text, re.DOTALL, re.S)

    only_text = re.sub(r"-----BEGIN PRIVACY-ENHANCED MESSAGE-----", "", only_text)
    only_text = re.sub(r"-----END PRIVACY-ENHANCED MESSAGE-----", "", only_text)

    headermatch =  RE_SEC_HEADER.search(only_text)

    header = ''
    if headermatch:
        header = headermatch.group()
        only_text = only_text.replace(header, '')

    only_text, parse_res = get_text_selectolax(only_text)

    only_text = re.sub(r"<.*?>", "", only_text, re.DOTALL, re.S)

    # Remove non ascii chars
    only_text = ''.join(i if ord(i) < 128 else ' ' for i in only_text)

    original_chars = len(raw_data)
    current_chars = len(only_text)
    percent_kept = (current_chars / original_chars) * 100
    process_index = multiprocessing.current_process().name
    print("{:.2f} % ({}) {}    ----   {}".format(percent_kept, process_index, dest_path, parse_res))

    with open(dest_path, 'w') as f:
        f.write(FILE_STATS.format(
            original_chars=original_chars,
            current_chars=current_chars,
            percent_kept=percent_kept,
        ))
        f.write(header)
        f.write(only_text)



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
    n_process = multiprocessing.cpu_count() * 2
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
