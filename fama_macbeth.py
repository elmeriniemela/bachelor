

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
    model = sm.OLS(y, X).fit()
    return model.params


def fama_macbeth(master):
    ff_categories = [str(n) for n in range(2, 49)]
    outcome_var = 'median_filing_period_returns'
    predictor_vars = ['percent_negative', 'log_size', 'log_turnover', 'log_book_to_market']
    profiling_vars = predictor_vars + [outcome_var, 'median_filing_period_value_weighted_returns', 'size', 'book_to_market', 'turnover']
    predictor_vars.extend(ff_categories)
    
    cross_sections = master.groupby(by=['year', 'quater'])
    cross_section_results = cross_sections.apply(ols_coef, outcome_var, predictor_vars)
    
    newey_west_df = pd.DataFrame(columns=['variable', 'coef', 'std_err', 'p_values', 't_values'])
    newey_west_df = newey_west_df.set_index(['variable'])
    for column_hat in cross_section_results:
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

    print(newey_west_df)
    """
                        coef   std_err  p_values  t_values
variable                                                  
const              -0.004102  0.002858  0.151159 -1.435450
percent_negative    0.000752  0.000537  0.161909  1.398679
log_size            0.000307  0.000241  0.201967  1.275968
log_turnover       -0.000260  0.000496  0.600079 -0.524287
log_book_to_market  0.000499  0.000334  0.135807  1.491589
2                   0.001769  0.001747  0.311413  1.012262
3                   0.002033  0.001823  0.264948  1.114773
4                  -0.001295  0.002170  0.550745 -0.596644
5                   0.000559  0.000951  0.556464  0.588102
6                   0.001103  0.001866  0.554502  0.591027
7                   0.001760  0.002314  0.446910  0.760576
8                   0.001278  0.001860  0.491880  0.687321
9                  -0.000321  0.001730  0.852843 -0.185493
10                  0.003556  0.001477  0.016067  2.407395
11                  0.002487  0.002148  0.246928  1.157842
12                  0.001980  0.001848  0.283992  1.071394
13                  0.000284  0.001845  0.877688  0.153900
14                  0.001972  0.001519  0.194026  1.298762
15                  0.002523  0.003567  0.479460  0.707172
16                 -0.002133  0.003520  0.544597 -0.605877
17                  0.001607  0.001816  0.376149  0.885015
18                 -0.001848  0.002076  0.373451 -0.890028
19                  0.002681  0.001927  0.164180  1.391150
20                  0.001279  0.002099  0.542326  0.609299
21                  0.000786  0.001576  0.617787  0.498989
22                  0.000425  0.001671  0.799260  0.254305
23                  0.000336  0.001906  0.860138  0.176199
24                  0.001040  0.001668  0.532882  0.623612
25                 -0.001234  0.003286  0.707353 -0.375413
26                  0.000451  0.001351  0.738764  0.333491
27                 -0.001977  0.001403  0.158861 -1.408912
28                 -0.001510  0.001699  0.374307 -0.888434
29                 -0.000838  0.001098  0.445605 -0.762763
30                 -0.001273  0.002177  0.558758 -0.584688
31                  0.000572  0.001519  0.706603  0.376423
32                  0.002085  0.002679  0.436349  0.778373
33                  0.001665  0.002243  0.457867  0.742364
34                  0.001420  0.001587  0.370750  0.895069
35                  0.001356  0.001648  0.410817  0.822457
36                  0.001131  0.001650  0.493031  0.685496
37                  0.001998  0.001675  0.232961  1.192765
38                 -0.001140  0.001551  0.462310 -0.735049
39                  0.001688  0.001578  0.284668  1.069891
40                 -0.001431  0.002108  0.497205 -0.678893
41                  0.001635  0.001717  0.341047  0.952098
42                  0.001760  0.001633  0.281046  1.077973
43                  0.001715  0.001589  0.280426  1.079363
44                  0.001439  0.002477  0.561251  0.580984
45                 -0.000575  0.001764  0.744654 -0.325697
46                  0.001128  0.002075  0.586608  0.543759
47                  0.001753  0.002347  0.455095  0.746948
48                 -0.000017  0.001601  0.991679 -0.010430
"""


def do_analysis(MAIN):
    master = get_master(MAIN)
    fama_macbeth(master)


def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        do_analysis(MAIN)


if __name__ == '__main__':
    main()