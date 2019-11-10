import os



"""
    Predefined SEC form strings
    Feel free to add your own lists
    ND-SRAF / McDonald : 201606
"""

f_10K = ['10-K', '10-K405', '10KSB', '10-KSB', '10KSB40']
f_10KA = ['10-K/A', '10-K405/A', '10KSB/A', '10-KSB/A', '10KSB40/A']
f_10KT = ['10-KT', '10KT405', '10-KT/A', '10KT405/A']
f_10Q = ['10-Q', '10QSB', '10-QSB']
f_10QA = ['10-Q/A', '10QSB/A', '10-QSB/A']
f_10QT = ['10-QT', '10-QT/A']
# List of all 10-X related forms
f_10X = f_10K + f_10KA + f_10KT + f_10Q + f_10QA + f_10QT
f_10K_X = f_10K + f_10KA + f_10KT
f_10Q_X = f_10Q + f_10QA + f_10QT
# Regulation A+ related forms
f_1X = ['1-A', '1-A/A', '1-K', '1-SA', '1-U', '1-Z']


# -----------------------
# User defined parameters
# -----------------------

# List target forms as strings separated by commas (case sensitive) or
#   load from EDGAR_Forms.  (See EDGAR_Forms module for predefined lists.)
PARM_FORMS = f_10K_X  # or, for example, PARM_FORMS = ['8-K', '8-K/A']
# 2008-2011 already zipped
PARM_BGNYEAR = 1994  # User selected bgn period.  Earliest available is 1994
PARM_ENDYEAR = 2008  # User selected end period.
PARM_BGNQTR = 1  # Beginning quarter of each year
PARM_ENDQTR = 4  # Ending quarter of each year
# Path where you will store the downloaded files
PARM_PATH = 'data/'
# Change the file pointer below to reflect your location for the log file
PARM_LOGFILE = ('logs/EDGAR_Download_FORM-X_LogFile_' +
                str(PARM_BGNYEAR) + '-' + str(PARM_ENDYEAR) + '.txt')

os.makedirs(os.path.dirname(PARM_LOGFILE), exist_ok=True)
os.makedirs(PARM_PATH, exist_ok=True)

YEARS_LIST = list(range(PARM_BGNYEAR, PARM_ENDYEAR + 1))
FILE_LIST = [PARM_PATH + str(year) + '.zip' for year in YEARS_LIST]
# EDGAR parameter
PARM_EDGARPREFIX = 'https://www.sec.gov/Archives/'

PERMNO_DB_NAME = "PERMNO.db"
MAIN_DB_NAME = "MAIN.db"
ALL_STOCKS_DB_NAME = "ALL_STOCKS.db"
MASTER_DICT_PATH = 'original_files/LoughranMcDonald_MasterDictionary_2018.csv'
