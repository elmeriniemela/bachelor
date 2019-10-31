

from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import pandas_profiling
import statsmodels.formula.api as smf


def get_master(MAIN):
    master = pd.read_sql("select * from master_edited", MAIN, index_col='index')

    # Mapping for renaming the colums for profiling
    useful_columns = [
        'price_minus_one_day',
        'volume_minus_one_day',
        'shares_outstanding_minus_one_day',
        'median_filing_period_returns', 
        'median_filing_period_value_weighted_returns',
        'number_of_words', 
        'percent_negative',
        'book_value_per_share',
        'ff_industry',
        'turnover',
        'year',
        'quater',
    ]

    # Select only specific columns
    master = master[useful_columns]


    # Calculate base values and cast types
    master['book_value_per_share'] = master['book_value_per_share'].astype(float)
    # Price per share * shares outstanding
    master['size'] = master.price_minus_one_day * master.shares_outstanding_minus_one_day
    #  Book Value Per Share / Price per share
    master['book_to_market'] = master.book_value_per_share / master.price_minus_one_day


    # FILTERING

    # Book-to-market COMPUSTAT data available and book value>0
    master = master[master['book_to_market'] > 0]
    # Price on filing date day minus one≥$3
    master = master[master['price_minus_one_day'] >= 3]
    # Number of words in 10-K >= 2,000
    master = master[master['number_of_words'] >= 2000]

    # Eliminate all rows containing infinite and not nan values 
    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')


    # WINSORIZE

    # we winsorize the book-to-market variable at the 1% level.
    master['book_to_market'] = winsorize(master['book_to_market'], limits=(0.01, 0.01))
    # master['percent_negative'] = winsorize(master['percent_negative'], limits=(0.01, 0.01))
    # master['median_filing_period_returns'] = winsorize(master['median_filing_period_returns'], limits=(0.01, 0.01))
    # master['turnover'] = winsorize(master['turnover'], limits=(0.01, 0.01))
    # master['size'] = winsorize(master['size'], limits=(0.01, 0.01))


    # LOG

    # Use log values for regression
    master['log_size'] = np.log(master['size'])
    master['log_book_to_market'] = np.log(master['book_to_market'])
    master['log_turnover'] = np.log(master['turnover'])

    # Create 48 - 1 FF industry dummies
    master = pd.concat([master, pd.get_dummies(master['ff_industry'], drop_first=True)], axis=1)

    return master


def ols_coef(section, outcome_var, predictor_vars):
    X = section[predictor_vars]
    y = section[outcome_var]
    X = sm.add_constant(X)
    # Should the Newey-West standard errors with one lag be here?
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags':1})
    return model.params


def fm_summary(cross_section_results):
    df = cross_section_results.describe().T
    df['std_error'] = df['std'] / np.sqrt(df['count'])
    df['tstat'] = df['mean'] / df['std_error']
    return df[['mean', 'std_error', 'tstat']]


def fama_macbeth(master):
    ff_categories = [str(n) for n in range(2, 49)]
    outcome_var = 'median_filing_period_returns'
    predictor_vars = ['percent_negative', 'log_size', 'log_turnover', 'log_book_to_market']
    profiling_vars = predictor_vars + [outcome_var, 'median_filing_period_value_weighted_returns', 'size', 'book_to_market', 'turnover']
    predictor_vars.extend(ff_categories)
    
    cross_sections = master.groupby(by=['year', 'quater'])
    cross_section_results = cross_sections.apply(ols_coef, outcome_var, predictor_vars)

    print(fm_summary(cross_section_results))
    """
                            mean  std_error     tstat
    const              -0.004102   0.002938 -1.396354
    percent_negative    0.000752   0.000506  1.484441
    log_size            0.000307   0.000243  1.266415
    log_turnover       -0.000260   0.000484 -0.537503
    log_book_to_market  0.000499   0.000347  1.439187
    2                   0.001769   0.001926  0.918280
    3                   0.002033   0.001946  1.044765
    4                  -0.001295   0.001990 -0.650534
    5                   0.000559   0.000968  0.577335
    6                   0.001103   0.002240  0.492145
    7                   0.001760   0.002343  0.750959
    8                   0.001278   0.002219  0.576191
    9                  -0.000321   0.002253 -0.142423
    10                  0.003556   0.001528  2.326531
    11                  0.002487   0.002515  0.988530
    12                  0.001980   0.002007  0.986376
    13                  0.000284   0.001999  0.142081
    14                  0.001972   0.001858  1.061448
    15                  0.002523   0.003821  0.660274
    16                 -0.002133   0.003630 -0.587500
    17                  0.001607   0.002077  0.773751
    18                 -0.001848   0.002158 -0.856188
    19                  0.002681   0.002187  1.225974
    20                  0.001279   0.002214  0.577624
    21                  0.000786   0.001822  0.431542
    22                  0.000425   0.001897  0.223998
    23                  0.000336   0.002224  0.150947
    24                  0.001040   0.002008  0.518110
    25                 -0.001234   0.003278 -0.376307
    26                  0.000451   0.001394  0.323325
    27                 -0.001977   0.001428 -1.383822
    28                 -0.001510   0.001679 -0.899448
    29                 -0.000838   0.001057 -0.792313
    30                 -0.001273   0.002128 -0.598142
    31                  0.000572   0.001776  0.322115
    32                  0.002085   0.002486  0.838956
    33                  0.001665   0.002075  0.802316
    34                  0.001420   0.001877  0.756790
    35                  0.001356   0.001830  0.740724
    36                  0.001131   0.001988  0.568797
    37                  0.001998   0.001947  1.025898
    38                 -0.001140   0.001729 -0.659183
    39                  0.001688   0.001734  0.973625
    40                 -0.001431   0.002414 -0.592949
    41                  0.001635   0.001973  0.828454
    42                  0.001760   0.001731  1.017185
    43                  0.001715   0.001812  0.946520
    44                  0.001439   0.002767  0.520167
    45                 -0.000575   0.001749 -0.328479
    46                  0.001128   0.002106  0.535805
    47                  0.001753   0.002630  0.666657
    48                 -0.000017   0.002053 -0.008133
    
    """


def do_analysis(MAIN):
    master = get_master(MAIN)
    fama_macbeth(master)


def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        do_analysis(MAIN)


if __name__ == '__main__':
    main()