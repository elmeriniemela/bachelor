

from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import pandas_profiling

def do_analysis(MAIN):
    master = pd.read_sql("select * from master_edited", MAIN, index_col='rowid')

    # Calculate base values and cast types
    master['bkvlps'] = master['bkvlps'].astype(float)
    master['size'] = master.price_minus_one_day * master.shares_outstanding
    master['book_to_market'] = master.bkvlps / master.price_minus_one_day

    # Book-to-market COMPUSTAT data available and book value>0
    master = master[master['book_to_market'] > 0]
    # Price on filing date day minus one≥$3
    master = master[master['price_minus_one_day'] >= 3]
    # Number of words in 10-K >= 2,000
    master = master[master['number of words'] >= 2000]

    # Eliminate all rows containing infinite and not nan values 
    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')

    # we winsorize the book-to-marketvariable at the 1% level.

    master['book_to_market'] = winsorize(master['book_to_market'], limits=(0.01, 0.01))


    # Use log values for regression
    master['log_size'] = np.log(master['size'])
    master['log_book_to_market'] = np.log(master['book_to_market'])
    master['log_turnover'] = np.log(master['turnover'])


    # Create 48 - 1 FF industry dummies
    master = pd.concat([master, pd.get_dummies(master['ff_industry'], drop_first=True)], axis=1)


    ff_categories = [str(n) for n in range(2, 49)]

    outcome_var = 'median_RET'
    predictor_vars = ['% negative', 'log_size', 'log_turnover', 'log_book_to_market']
    profiling_vars = [var for var in predictor_vars] + [outcome_var]


    predictor_vars.extend(ff_categories)



    summary_df = master[profiling_vars]
    profile = summary_df.profile_report(title='Data Profiling Report')
    profile.to_file(output_file="profile.html")


    
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