

from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import pandas_profiling

def do_profiling(master, profiling_vars):
    print("Creating profiling...")
    summary_df = master[profiling_vars]
    profile = summary_df.profile_report(title='Data Profiling Report')
    profile.to_file(output_file="index.html")


def do_analysis(MAIN):
    master = pd.read_sql("select * from master_edited", MAIN, index_col='rowid')

    useful_columns = {
        'price_minus_one_day': 'price_minus_one_day', 
        'volume': 'volume',
        'shares_outstanding': 'shares_outstanding',
        'median_RET': 'median_filing_period_returns', 
        'median_vwretd': 'median_filing_period_value_weighted_returns',
        'number of words': 'number_of_words', 
        '% negative': '%_negative',
        'bkvlps': 'book_value_per_share',
        'ff_industry': 'ff_industry',
        'turnover': 'turnover',
    }

    master = master[useful_columns.keys()]
    master.columns = useful_columns.values()


    # Calculate base values and cast types
    master['book_value_per_share'] = master['book_value_per_share'].astype(float)

    # Price per share * shares outstanding
    master['size'] = master.price_minus_one_day * master.shares_outstanding
    #  Book Value Per Share / Price per share
    master['book_to_market'] = master.book_value_per_share / master.price_minus_one_day

    # Book-to-market COMPUSTAT data available and book value>0
    master = master[master['book_to_market'] > 0]
    # Price on filing date day minus one≥$3
    master = master[master['price_minus_one_day'] >= 3]
    # Number of words in 10-K >= 2,000
    master = master[master['number_of_words'] >= 2000]

    # Eliminate all rows containing infinite and not nan values 
    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')

    # we winsorize the book-to-market variable at the 1% level.
    master['book_to_market'] = winsorize(master['book_to_market'], limits=(0.01, 0.01))
    # master['%_negative'] = winsorize(master['%_negative'], limits=(0.01, 0.01))
    # master['median_filing_period_returns'] = winsorize(master['median_filing_period_returns'], limits=(0.01, 0.01))
    # master['turnover'] = winsorize(master['turnover'], limits=(0.01, 0.01))
    # master['size'] = winsorize(master['size'], limits=(0.01, 0.01))

    # Use log values for regression
    master['log_size'] = np.log(master['size'])
    master['log_book_to_market'] = np.log(master['book_to_market'])
    master['log_turnover'] = np.log(master['turnover'])

    # Create 48 - 1 FF industry dummies
    master = pd.concat([master, pd.get_dummies(master['ff_industry'], drop_first=True)], axis=1)

    ff_categories = [str(n) for n in range(2, 49)]

    outcome_var = 'median_filing_period_returns'
    predictor_vars = ['%_negative', 'log_size', 'log_turnover', 'log_book_to_market']
    profiling_vars = predictor_vars + [outcome_var, 'median_filing_period_value_weighted_returns', 'size', 'book_to_market', 'turnover']

    do_profiling(master, profiling_vars)

    # Binary values don't work in profiling, so add them after
    predictor_vars.extend(ff_categories)
    
    X = master[predictor_vars]
    y = master[outcome_var]

    # Add constant to regression
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())


def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        do_analysis(MAIN)


if __name__ == '__main__':
    main()