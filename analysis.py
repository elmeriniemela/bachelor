import imgkit
import subprocess
from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import pandas_profiling

BOOTSTRAP = """
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
"""


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
    filtering_summary_rows = []
    master = pd.read_sql("select * from master_edited where year>=%s and year<=%s" % (year_bgn, year_end), MAIN, index_col='index')
    master = master[(master['form'].str.upper() == '10-K') | (master['form'].str.upper() == '10-K405')]
    filtering_summary_rows.append((
        "Full 10-K Document EDGAR 10-K/10-K405 {}-{} complete sample".format(year_bgn, year_end),
        len(master),
        ''
    ))
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
    ]
    filtering_columns = useful_columns + [
        'fname',
        'LPERMNO',
        'LPERMCO',
    ]

    # Select only specific columns
    master = master[filtering_columns]

    OLD_LEN = len(master)
    # Include only first filing in a given year
    master = master[master['fname'].str.endswith("_1.txt")]
    filtering_summary_rows.append((
        "Include only first filing in a given year",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master = master[np.isfinite(master['LPERMNO'])]
    filtering_summary_rows.append((
        "CRSP PERMNO match",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master = master[np.isfinite(master['price_minus_one_day'])]
    master = master[np.isfinite(master['shares_outstanding_minus_one_day'])]
    filtering_summary_rows.append((
        "CRSP market capitalization data available",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    # Price on filing date day minus one&ge;$3
    master = master[master['price_minus_one_day'] >= 3]
    filtering_summary_rows.append((
        "Price on filing date day minus one is greater than $3",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master = master[np.isfinite(master['RET_qeom'])]
    filtering_summary_rows.append((
        "Returns for day 0-3 event period",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))


    master = master[np.isfinite(master['turnover'])]
    master = master[master['turnover'] != 0]
    filtering_summary_rows.append((
        "At least 60 days of volume prior to file date (used to caluclate turnover)",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master['book_value_per_share'] = master['book_value_per_share'].astype(float)
    master = master[np.isfinite(master['book_value_per_share'])]
    master = master[master['book_value_per_share'] > 0]
    filtering_summary_rows.append((
        "Book-to-market COMPUSTAT data available and book value greater than zero",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master = master[master['number_of_words'] >= 2000]
    filtering_summary_rows.append((
        "Atleast 2,000 words in 10-K",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))

    master = master[useful_columns]




    # Calculate base values and cast types
    # Price per share * shares outstanding
    master['size'] = master.price_minus_one_day * master.shares_outstanding_minus_one_day
    #  Book Value Per Share / Price per share
    master['book_to_market'] = master.book_value_per_share / master.price_minus_one_day

    master['excess_returns'] = master.RET_qeom - master.market_vwretd_qeom


    # Eliminate all rows containing infinite and not nan values 
    master.replace([np.inf, -np.inf], np.nan, inplace=True)
    master = master.dropna(how='any')
    filtering_summary_rows.append((
        "Rows containing any missing values",
        len(master),
        filtering_summary_rows[-1][1] - len(master)
    ))
    # Display as percentage insted of decimal
    master.loc[:,'excess_returns'] *= 100


    # This should have been done in data_organize.py since shares_outstanding was expressed in thousands
    master.loc[:,'turnover'] /= 1000

    # Shares outstanding is in thousands so to get size in billions we will divide by million
    master.loc[:,'size'] /= 1_000_000

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


    # In all cases, the excess return refers to the firm’s buy-and-hold stock return
    # minus the CRSP value-weighted buy-and-hold market indexreturn over the 4-day event window.

    # event period excess return defined as the firm’s buy-and-hold stock return
    # minus the CRSP value-weighted buy-and-hold market index return
    # over the 4-day event window, expressed as a percent.
    outcome_var = 'excess_returns'
    predictor_vars = [
        'percent_negative', 
        'log_size', 
        'log_turnover', 
        'log_book_to_market',
        'nasdaq_dummy'
    ]
    ff_categories = [n for n in master['ff_industry'].unique() if n in master.columns]
    predictor_vars.extend(ff_categories)

    return master, outcome_var, predictor_vars, filtering_summary_rows
    

def ols_coef(section, outcome_var, predictor_vars, len_N):
    X = section[predictor_vars]
    y = section[outcome_var]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    series = model.params

    # The estimates for each period are weighted by frequency, 
    # since the calendar distribution of file dates is clustered 
    # around specific dates (see Griffin (2003)).
    series *= len(section) / len_N

    # Add r_squared so we can take the mean later
    series['r_squared'] = model.rsquared_adj
    
    return series


def do_fama_macbeth_analysis(MAIN, year_bgn, year_end):
    master, outcome_var, predictor_vars, _ = prepare_analysis(MAIN, year_bgn, year_end)
    
    cross_sections = master.groupby(by=['year', 'quater'])
    cross_section_results = cross_sections.apply(ols_coef, outcome_var, predictor_vars, len(master))
    print(cross_section_results)
    newey_west_df = pd.DataFrame(columns=['Variable name', 'Coefficient', 'Standard Error', 'T-Value'])
    newey_west_df = newey_west_df.set_index(['Variable name'])
    for column_hat in cross_section_results:
        if column_hat in {'r_squared', 'const'}:
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
            model.tvalues[0], # t_values
        ]
        newey_west_df.loc[column_hat] = row

    fname = "docs/results{}-{}.html".format(year_bgn, year_end)
    mapping = {
        'percent_negative': 'Negative Word Frequency',
        'log_size': 'Log(size)',
        'log_turnover': 'Log(turnover)',
        'log_book_to_market': 'Log(book-to-market)',
        'nasdaq_dummy': 'NASDAQ Dummy',
    }
    newey_west_df = newey_west_df.head(len(mapping))
    newey_west_df.rename(index=mapping, inplace=True)
    print(newey_west_df)

    with open(fname, 'w') as f_obj:
        f_obj.write(BOOTSTRAP)
        f_obj.write(newey_west_df.to_html(classes=["table"]).replace('border="1"', ''))
        f_obj.write("<br/>\n")
        f_obj.write("<b style='margin: 1.5rem !important; font-size: 20px'>Average Adjusted R-Squared: {:.2f} %</b>".format(cross_section_results['r_squared'].mean() * 100))


def do_summary_statistics(MAIN):
    master1, _, _, filtering_summary_rows1 = prepare_analysis(MAIN, 1994, 2008)
    master2, _, _, filtering_summary_rows2 = prepare_analysis(MAIN, 2008, 2018)


    filtering_summary_df = pd.DataFrame(columns=[str(i) for i in range(4)])
    filtering_summary_df.columns = pd.MultiIndex.from_product([
        ['Old Sample 1994-2008\n(N = {})'.format(len(master1)), 'New Sample 2008-2018\n(N = {})'.format(len(master2))], 
        ['Sample Size', 'Observations\nRemoved']
    ])
    filtering_summary_df.index = pd.Index([], name='Source/Filter')

    for row1, row2 in zip(filtering_summary_rows1, filtering_summary_rows2):
        filter_name, sample1, removed1 = row1
        filter_name, sample2, removed2 = row2
        row = [
            sample1,
            removed1,
            sample2,
            removed2,
        ]
        filtering_summary_df.loc[filter_name] = row

    with open('docs/filtering_summary.html', 'w') as f_obj:
        f_obj.write(BOOTSTRAP)
        f_obj.write(filtering_summary_df.to_html(classes=["table"])\
            .replace('border="1"', '')\
            .replace('\\n', '<br/>')
        )





    master1.loc[:,'nasdaq_dummy'] *= 100
    master2.loc[:,'nasdaq_dummy'] *= 100

    summary_df = pd.DataFrame(columns=[str(i) for i in range(6)])
    summary_df.columns = pd.MultiIndex.from_product([
        ['Old Sample 1994-2008\n(N = {})'.format(len(master1)), 'New Sample 2008-2018\n(N = {})'.format(len(master2))], 
        ['Mean', 'Median', 'Standard Deviation']
    ])
    summary_df.index = pd.Index([], name='Variable Name')

    summary_vars =  [
        ('percent_negative', 'Negative Word Frequency', '%'),
        ('excess_returns', 'Event period [0, 3] excess return', '%'),
        ('size', 'Size (billions $)', '$'),
        ('turnover', 'Turnover', ''),
        ('book_to_market', 'Book-to-market', ''),
        ('nasdaq_dummy', 'NASDAQ Dummy', '%'),
    ]


    for var, new_name, char in summary_vars:
        row = [
            '{:.2f}{}'.format(master1[var].mean(), char),
            '{:.2f}{}'.format(master1[var].median(), char),
            '{:.2f}{}'.format(master1[var].std(), char),
            '{:.2f}{}'.format(master2[var].mean(), char),
            '{:.2f}{}'.format(master2[var].median(), char),
            '{:.2f}{}'.format(master2[var].std(), char),
        ]
        summary_df.loc[new_name] = row

    with open("docs/summary_statistics.html", 'w') as f_obj:
        f_obj.write(BOOTSTRAP)
        f_obj.write(summary_df.to_html(classes=["table"])\
            .replace('border="1"', '')\
            .replace('\\n', '<br/>')
        )

    print(summary_df)


def do_quantile_graph(MAIN):
    master, _, _, _= prepare_analysis(MAIN, 1994, 2008)

    X = 'Quintile (based on proportion of negative words)'

    master[X] = pd.qcut(master['percent_negative'], q=5)
    series = master.groupby(by=[X]).apply(lambda df: df['excess_returns'].median())
    series.index = pd.Index(['Low', '2', '3', '4', 'High'], name=X)
    plotted = series.plot(label='Old Sample (1994-2008)')
    plotted.set_ylabel('Median Filing Period Excess Return')

    master, _, _, _ = prepare_analysis(MAIN, 2008, 2018)

    master[X] = pd.qcut(master['percent_negative'], q=5)
    series = master.groupby(by=[X]).apply(lambda df: df['excess_returns'].median())
    series.index = pd.Index(['Low', '2', '3', '4', 'High'], name=X)
    plotted = series.plot(label='New Sample (2008-2018)')
    plt.legend()
    plt.show()



def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        # do_fama_macbeth_analysis(MAIN, 1994, 2008)
        # do_fama_macbeth_analysis(MAIN, 2008, 2018)
        # do_sample_profiling(MAIN, 2008, 2018, 'index.html')
        # do_full_data_profiling(MAIN, 2008, 2018, 'full_dataset.html')
        # do_sample_profiling(MAIN, 1994, 2008, 'original_study_sample.html')
        # do_full_data_profiling(MAIN, 1994, 2008, 'original_study_full_dataset.html')
        # do_summary_statistics(MAIN)
        do_quantile_graph(MAIN)


if __name__ == '__main__':
    main()