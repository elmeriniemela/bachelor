 
Problems in data:
* Turnover: mean 2369.141695 compared to 1.519
* Event period [0,3] excess return: mean 0.0004461367954 compared to −0.12%
https://wrds-web.wharton.upenn.edu/wrds/query_forms/variable_documentation.cfm?vendorCode=CRSP&libraryCode=crspa&fileCode=dsf&id=ret

* Outliers in turnover, size, median_filing_period_returns, %_negative


                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     median_filing_period_returns   R-squared:                       0.005
Model:                                      OLS   Adj. R-squared:                  0.004
Method:                           Least Squares   F-statistic:                     3.110
Date:                          Tue, 29 Oct 2019   Prob (F-statistic):           6.37e-13
Time:                                  10:48:16   Log-Likelihood:                 77552.
No. Observations:                         29270   AIC:                        -1.550e+05
Df Residuals:                             29218   BIC:                        -1.546e+05
Df Model:                                    51                                         
Covariance Type:                      nonrobust                                         
======================================================================================
                         coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------------
const                 -0.0015      0.002     -0.722      0.470      -0.006       0.003
%_negative             0.0002      0.000      1.542      0.123   -6.65e-05       0.001
log_size               0.0004   5.99e-05      6.700      0.000       0.000       0.001
log_turnover          -0.0007      0.000     -6.157      0.000      -0.001      -0.000
log_book_to_market     0.0004      0.000      3.252      0.001       0.000       0.001
2                      0.0017      0.002      0.837      0.403      -0.002       0.006
3                      0.0035      0.002      1.504      0.133      -0.001       0.008
4                      0.0026      0.002      1.077      0.281      -0.002       0.007
5                      0.0030      0.003      0.874      0.382      -0.004       0.010
6                      0.0034      0.002      1.497      0.134      -0.001       0.008
7                      0.0008      0.002      0.359      0.720      -0.003       0.005
8                      0.0020      0.002      0.897      0.370      -0.002       0.006
9                      0.0015      0.002      0.732      0.464      -0.003       0.006
10                     0.0041      0.002      1.906      0.057      -0.000       0.008
11                     0.0028      0.002      1.335      0.182      -0.001       0.007
12                     0.0014      0.002      0.714      0.475      -0.002       0.005
13                     0.0009      0.002      0.458      0.647      -0.003       0.005
14                     0.0023      0.002      1.132      0.258      -0.002       0.006
15                     0.0029      0.002      1.226      0.220      -0.002       0.008
16                    -0.0033      0.003     -1.251      0.211      -0.008       0.002
17                     0.0011      0.002      0.521      0.603      -0.003       0.005
18                     0.0008      0.002      0.380      0.704      -0.003       0.005
19                     0.0029      0.002      1.366      0.172      -0.001       0.007
20                     0.0025      0.003      0.932      0.351      -0.003       0.008
21                     0.0008      0.002      0.400      0.689      -0.003       0.005
22                  7.531e-05      0.002      0.037      0.971      -0.004       0.004
23                     0.0015      0.002      0.723      0.470      -0.003       0.006
24                     0.0030      0.002      1.356      0.175      -0.001       0.007
25                     0.0010      0.003      0.344      0.731      -0.005       0.007
26                     0.0007      0.003      0.264      0.792      -0.005       0.006
27                    -0.0011      0.002     -0.460      0.646      -0.006       0.004
28                  2.235e-05      0.002      0.010      0.992      -0.004       0.004
29                     0.0003      0.003      0.136      0.892      -0.005       0.005
30                     0.0014      0.002      0.739      0.460      -0.002       0.005
31                    -0.0007      0.002     -0.366      0.714      -0.005       0.003
32                     0.0016      0.002      0.819      0.413      -0.002       0.006
33                     0.0026      0.002      1.246      0.213      -0.002       0.007
34                     0.0017      0.002      0.894      0.372      -0.002       0.006
35                     0.0025      0.002      1.259      0.208      -0.001       0.006
36                     0.0014      0.002      0.696      0.486      -0.002       0.005
37                     0.0024      0.002      1.154      0.248      -0.002       0.006
38                     0.0007      0.002      0.310      0.757      -0.004       0.005
39                     0.0027      0.003      1.047      0.295      -0.002       0.008
40                     0.0010      0.002      0.476      0.634      -0.003       0.005
41                     0.0022      0.002      1.131      0.258      -0.002       0.006
42                     0.0031      0.002      1.558      0.119      -0.001       0.007
43                     0.0022      0.002      1.081      0.279      -0.002       0.006
44                     0.0019      0.002      0.836      0.403      -0.003       0.006
45                     0.0018      0.002      0.799      0.425      -0.003       0.006
46                     0.0023      0.002      0.965      0.335      -0.002       0.007
47                     0.0015      0.002      0.761      0.447      -0.002       0.005
48                     0.0022      0.002      1.114      0.265      -0.002       0.006
==============================================================================
Omnibus:                    14569.929   Durbin-Watson:                   1.985
Prob(Omnibus):                  0.000   Jarque-Bera (JB):          2521182.775
Skew:                           1.317   Prob(JB):                         0.00
Kurtosis:                      48.391   Cond. No.                     2.12e+03
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
