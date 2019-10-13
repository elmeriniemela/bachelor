from nltk.tokenize import word_tokenize
from sqlite3 import connect
import pandas as pd

from helpers import load_masterdictionary

import constants as C

def word_frequency():
    lm = load_masterdictionary('original_files/LoughranMcDonald_MasterDictionary_2018.csv')
    freq = {key: None for key in list(lm.keys()) + ['fname']}
    freq_sorted = sorted(freq.items(), key=lambda t: t[0])
    print(freq_sorted)
    # with connect(C.MAIN_DB_NAME) as MAIN:
    #     paths = 


if __name__ == "__main__":
    word_frequency()