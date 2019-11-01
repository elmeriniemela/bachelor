 
Problems in data:
* Turnover: mean 2369.141695 compared to 1.519
* Event period [0,3] excess return: mean 0.0004461367954 compared to −0.12%
https://wrds-web.wharton.upenn.edu/wrds/query_forms/variable_documentation.cfm?vendorCode=CRSP&libraryCode=crspa&fileCode=dsf&id=ret

* Outliers in turnover, size, median_filing_period_returns, %_negative


                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     median_filing_period_returns   R-squared:                       0.005
Model:                                      OLS   Adj. R-squared:                  0.002
Method:                           Least Squares   F-statistic:                     2.036
Date:                          Thu, 31 Oct 2019   Prob (F-statistic):           1.85e-05
Time:                                  16:22:36   Log-Likelihood:                 56786.
No. Observations:                         21490   AIC:                        -1.135e+05
Df Residuals:                             21438   BIC:                        -1.131e+05
Df Model:                                    51                                         
Covariance Type:                      nonrobust                                         
======================================================================================
                         coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------------
const                 -0.0018      0.002     -0.742      0.458      -0.007       0.003
percent_negative       0.0004      0.000      1.998      0.046    7.05e-06       0.001
log_size               0.0004   7.41e-05      5.576      0.000       0.000       0.001
log_turnover          -0.0007      0.000     -4.606      0.000      -0.001      -0.000
log_book_to_market     0.0004      0.000      2.663      0.008       0.000       0.001
2                      0.0015      0.002      0.647      0.517      -0.003       0.006
3                      0.0006      0.003      0.230      0.818      -0.005       0.006
4                      0.0002      0.003      0.051      0.959      -0.006       0.006
5                      0.0021      0.004      0.483      0.629      -0.006       0.011
6                      0.0025      0.003      0.983      0.326      -0.002       0.008
7                      0.0009      0.002      0.360      0.719      -0.004       0.006
8                      0.0013      0.002      0.504      0.615      -0.004       0.006
9                      0.0015      0.002      0.622      0.534      -0.003       0.006
10                     0.0030      0.002      1.254      0.210      -0.002       0.008
11                     0.0028      0.002      1.206      0.228      -0.002       0.007
12                     0.0014      0.002      0.625      0.532      -0.003       0.006
13                     0.0008      0.002      0.348      0.728      -0.004       0.005
14                     0.0020      0.002      0.890      0.373      -0.002       0.006
15                     0.0022      0.003      0.821      0.412      -0.003       0.007
16                    -0.0037      0.003     -1.265      0.206      -0.009       0.002
17                     0.0013      0.002      0.556      0.579      -0.003       0.006
18                     0.0012      0.002      0.492      0.623      -0.003       0.006
19                     0.0027      0.002      1.153      0.249      -0.002       0.007
20                     0.0031      0.003      1.002      0.316      -0.003       0.009
21                     0.0009      0.002      0.423      0.672      -0.003       0.005
22                    -0.0002      0.002     -0.083      0.934      -0.005       0.004
23                     0.0019      0.002      0.818      0.413      -0.003       0.006
24                     0.0017      0.003      0.661      0.509      -0.003       0.007
25                     0.0012      0.003      0.380      0.704      -0.005       0.007
26                     0.0014      0.003      0.441      0.659      -0.005       0.008
27                    -0.0021      0.003     -0.677      0.498      -0.008       0.004
28                    -0.0018      0.003     -0.693      0.488      -0.007       0.003
29                 -1.281e-05      0.003     -0.005      0.996      -0.005       0.005
30                     0.0011      0.002      0.511      0.609      -0.003       0.005
31                    -0.0010      0.002     -0.440      0.660      -0.005       0.003
32                     0.0015      0.002      0.667      0.505      -0.003       0.006
33                     0.0024      0.002      1.008      0.313      -0.002       0.007
34                     0.0015      0.002      0.707      0.479      -0.003       0.006
35                     0.0023      0.002      1.018      0.309      -0.002       0.007
36                     0.0009      0.002      0.398      0.691      -0.003       0.005
37                     0.0020      0.002      0.872      0.383      -0.002       0.006
38                    -0.0004      0.002     -0.168      0.867      -0.005       0.004
39                     0.0018      0.003      0.543      0.587      -0.005       0.008
40                     0.0010      0.002      0.467      0.641      -0.003       0.005
41                     0.0016      0.002      0.713      0.476      -0.003       0.006
42                     0.0028      0.002      1.283      0.199      -0.001       0.007
43                     0.0021      0.002      0.906      0.365      -0.002       0.007
44                     0.0013      0.003      0.508      0.611      -0.004       0.007
45                     0.0004      0.003      0.172      0.863      -0.005       0.006
46                     0.0016      0.003      0.583      0.560      -0.004       0.007
47                     0.0009      0.002      0.399      0.690      -0.004       0.005
48                     0.0019      0.002      0.853      0.394      -0.002       0.006
==============================================================================
Omnibus:                    12680.185   Durbin-Watson:                   1.947
Prob(Omnibus):                  0.000   Jarque-Bera (JB):          2883568.748
Skew:                           1.722   Prob(JB):                         0.00
Kurtosis:                      59.644   Cond. No.                     2.01e+03
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
* Include robust standard errors.
* Do i need cross ectional Fama mac beth regressions
[2] The condition number is large, 2.12e+03. This might indicate that there are
strong multicollinearity or other numerical problems.
* No need to worry

start with introduction 5 pages
* motivation
* results
* litarature overview
* Writing tips for phd students



Questions:

* Why are all values so low? coef, std err, r-squared?


* Original study Table IV:
    * What do the numbers mean? Coefficients?
    * "Fama-French (1997) industry dummies (based on 48 industries) and a constant are also included in each regression."
    * This implies several regressions, but i did only one regression with multiple variables?

* Should i try my luck with R?


Econometrics notes:

* A larger variance of X reduces std err.
* A larger sample size T reduces std err

* R-squared:
    * The point of regression is to explain the variation in y as a function of x. 
    An important question is therefore: How much of the variation in y does x explain?
    * How does the regression fit the data (think of the scatterplot and regression line)?
    * R-squared is a number between 0 and 1, and is interpreted as the percentage of the variation in Y that can be explained by X
    * For a simple regression with a single explanatory variable R^2 = Correlation(x, y)^2.

* t-statistics measure the distance between the estimate and the (unknown) true valueof the parameter, relative to its standard error
* My Null hyphothises: negative word frequency (X) has no effect on median filing period returns (Y)
* When the null hypothesis is true, we know that the t-statistic is asymptoticallystandard normally distributed. We can therefore expect the t-statistic to be close to zero (which is the mean of the standard normal distribution)
* Reject the null hypothesis when the t-statistic is too extreme for the null hypothesis to be realistically true.


* P-values (probability values) indicate the probability that your result occurred bychance alone.
* Example: a p-value<5%, indicates that you can reject the null hyphothises at the 5% level.


* In finance research a 5% significance level is conventional, meaning that researchers often simply check whether the t-statistic is larger (in absolute value)than 1.96 (or roughly 2) to assess whetherxhas a significant effect ony.
