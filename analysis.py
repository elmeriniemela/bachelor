

from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import pandas_profiling

def do_full_data_profiling(MAIN, year_bgn, year_end, filename):
    print('Creating full data profiling from {} to {}. Saving to {}'.format(year_bgn, year_end, filename))
    profiling_vars = [
        'RET_qeom',
        'percent_negative', 
        'price_minus_one_day', 
        'shares_outstanding_minus_one_day', 
        'book_value_per_share',
        'market_vwretd_qeom',
        'turnover',
        'number_of_words',
        'nasdaq_dummy',
        'LPERMNO_unique',
        'year',
        'quater',
    ]
    master = pd.read_sql("select * from master_edited where year>=%s and year<=%s" % (year_bgn, year_end), MAIN, index_col='index')
    profile = master[profiling_vars].profile_report(title='Fulldata Profiling Report from {} to {}'.format(year_bgn, year_end))
    profile.to_file(output_file='docs/' + filename)
    print('Saved to {}'.format(filename))


def do_sample_profiling(MAIN, year_bgn, year_end, filename):
    print('Creating sample profiling from {} to {}. Saving to {}'.format(year_bgn, year_end, filename))
    master, outcome_var, _ = prepare_analysis(MAIN, year_bgn, year_end)

    profiling_vars = [
        outcome_var,
        'percent_negative', 
        'log_size', 
        'log_turnover', 
        'log_book_to_market',
        'market_vwretd_qeom',
        'size', 
        'book_to_market', 
        'turnover',
    ]

    profile = master[profiling_vars].profile_report(title='Data Sample analysis from {} to {}'.format(year_bgn, year_end))
    profile.to_file(output_file='docs/' + filename)
    print('Saved to {}'.format(filename))



def prepare_analysis(MAIN, year_bgn, year_end):
    master = pd.read_sql("select * from master_edited where year>=%s and year<=%s" % (year_bgn, year_end), MAIN, index_col='index')

    # Mapping for renaming the colums for profiling
    useful_columns = [
        'price_minus_one_day',
        'volume_minus_one_day',
        'shares_outstanding_minus_one_day',
        'RET_qeom', 
        'market_vwretd_qeom',
        'number_of_words', 
        'percent_negative',
        'book_value_per_share',
        'ff_industry',
        'nasdaq_dummy',
        'turnover',
        'year',
        'quater',
        'fname',
        # 'LPERMNO_unique',
    ]

    # Select only specific columns
    master = master[useful_columns]


    # Calculate base values and cast types
    master['book_value_per_share'] = master['book_value_per_share'].astype(float)
    # Price per share * shares outstanding
    master['size'] = master.price_minus_one_day * master.shares_outstanding_minus_one_day
    #  Book Value Per Share / Price per share
    master['book_to_market'] = master.book_value_per_share / master.price_minus_one_day

    master['excess_returns'] = master.RET_qeom - master.market_vwretd_qeom



    # FILTERING
    # Include only first filing in a given year
    master = master[master['fname'].str.endswith("_1.txt")]

    # Book-to-market COMPUSTAT data available and book value>0
    master = master[master['book_to_market'] > 0]
    # Price on filing date day minus one≥$3
    master = master[master['price_minus_one_day'] >= 3]
    # Number of words in 10-K >= 2,000
    master = master[master['number_of_words'] >= 2000]
    # master = master[master['year'] >= 2009]

    # Eliminate all rows containing infinite and not nan values 
    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')

    # Multiply coefficients
    # master.loc[:,'excess_returns'] *= 1000

    # WINSORIZE

    # we winsorize the book-to-market variable at the 1% level.
    master['book_to_market'] = winsorize(master['book_to_market'], limits=(0.01, 0.01))
    # master['percent_negative'] = winsorize(master['percent_negative'], limits=(0.01, 0.01))
    # master['RET_qeom'] = winsorize(master['RET_qeom'], limits=(0.01, 0.01))

    # LOG
    # Use log values for regression
    master['log_size'] = np.log(master['size'])
    master['log_book_to_market'] = np.log(master['book_to_market'])
    master['log_turnover'] = np.log(master['turnover'])

    # Create 48 - 1 FF industry dummies
    master = pd.concat([master, pd.get_dummies(master['ff_industry'], drop_first=True)], axis=1)

    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')


    # In all cases, the excess return refers to the firm’s buy-and-hold stock return
    # minus the CRSP value-weighted buy-and-hold market indexreturn over the 4-day event window.

    # event period excess return defined as the firm’s buy-and-hold stock return
    # minus the CRSP value-weighted buy-and-hold market index return
    # over the 4-day event window, expressed as a percent.
    outcome_var = 'excess_returns'
    predictor_vars = ['percent_negative', 'log_size', 'log_turnover', 'log_book_to_market', 'nasdaq_dummy']
    ff_categories = [n for n in master['ff_industry'].unique() if n in master.columns]
    predictor_vars.extend(ff_categories)

    return master, outcome_var, predictor_vars
    

def ols_coef(section, outcome_var, predictor_vars):
    X = section[predictor_vars]
    y = section[outcome_var]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    series = model.params
    # Add r_squared so we can take the mean later
    series['r_squared'] = model.rsquared_adj
    return series


def do_fama_macbeth_analysis(MAIN):
    master, outcome_var, predictor_vars = prepare_analysis(MAIN, C.PARM_BGNYEAR, C.PARM_ENDYEAR)
    
    cross_sections = master.groupby(by=['year', 'quater'])
    cross_section_results = cross_sections.apply(ols_coef, outcome_var, predictor_vars)
    print(cross_section_results)
    newey_west_df = pd.DataFrame(columns=['variable', 'coef', 'std_err', 'p_values', 't_values'])
    newey_west_df = newey_west_df.set_index(['variable'])
    for column_hat in cross_section_results:
        if column_hat == 'r_squared':
            # This is not supposed to be t tested
            # we saved it only for the average
            continue
        series = cross_section_results[column_hat]
        # Python doesn't accept OLS without X so lets fill it with 1
        X = np.ones((series.shape[0],1))
        y = series
        # Newey-West standard errors with one lag
        model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags':1})
        row = [
            model.params[0], # coef
            model.bse[0], # std_err
            model.pvalues[0], # p_values
            model.tvalues[0], # t_values
        ]
        newey_west_df.loc[column_hat] = row

    print("Average Adjusted R-Squared: ", cross_section_results['r_squared'].mean())
    print(newey_west_df)


def do_normal_analysis(MAIN):
    master, outcome_var, predictor_vars = prepare_analysis(MAIN, C.PARM_BGNYEAR, C.PARM_ENDYEAR)

    X = master[predictor_vars]
    y = master[outcome_var]

    # Add constant to regression
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())


def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        # do_normal_analysis(MAIN)
        # do_fama_macbeth_analysis(MAIN)
        do_sample_profiling(MAIN, 2008, 2018, 'index.html')
        do_full_data_profiling(MAIN, 2008, 2018, 'full_dataset.html')
        do_sample_profiling(MAIN, 1994, 2008, 'original_study_sample.html')
        do_full_data_profiling(MAIN, 1994, 2008, 'original_study_full_dataset.html')


if __name__ == '__main__':
    main()