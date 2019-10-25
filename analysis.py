

from sqlite3 import connect
import statsmodels.api as sm
import numpy as np
import pandas as pd
import constants as C
import matplotlib.pyplot as plt

def do_analysis(MAIN):
    master = pd.read_sql("select * from master_edited", MAIN, index_col='rowid')

    master['bkvlps'] = master['bkvlps'].astype(float)
    master['size'] = master.volume * master.shares_outstanding
    master['log_size'] = np.log(master['size'])
    master['book_to_market'] = master.bkvlps / master.size
    master['log_book_to_market'] = np.log(master['book_to_market'])

    master.replace([np.inf, -np.inf], np.nan, inplace=True)

    master = pd.concat([master, pd.get_dummies(master['ff_industry'], drop_first=True)], axis=1)

    cleaned = master.dropna(how='any')
    

    import pdb; pdb.set_trace()

    # ff_categories = [str(n) for n in range(2, 49)]

    X = cleaned[['% negative', 'log_size', 'log_book_to_market']] # + ff_categories]
    print(X)
    y = cleaned['median_RET']
    print(y)


    model = sm.OLS(y, X).fit()
    print(model.summary())


def main():
    with connect(C.MAIN_DB_NAME) as MAIN:
        do_analysis(MAIN)


if __name__ == '__main__':
    main()