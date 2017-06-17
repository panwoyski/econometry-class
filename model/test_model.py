import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as stats

def test_stationarity(timeseries, window=12):
    # Determing rolling statistics
    rolmean = timeseries.rolling(center=False, window=window).mean()
    rolstd = timeseries.rolling(center=False, window=window).std()

    # Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = stats.tsa.stattools.adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)


def date_parser(str_date):
    return pd.datetime.strptime(str_date, '%Y/%m')

filename = 'commits_by_month.csv'
commits_series = pd.read_csv(
    filename,
    sep=',',
    header=0,
    parse_dates=[0],
    index_col=0,
    squeeze=True,
    date_parser=date_parser
).astype('float')


def generate_diff_series(timeseries):
    return (timeseries - timeseries.shift()).dropna()

# test_stationarity(commits_series)
diff1 = generate_diff_series(commits_series)
# test_stationarity(diff1)
lag_acf = stats.tsa.stattools.acf(diff1, nlags=15)
lag_pacf = stats.tsa.stattools.pacf(diff1, nlags=15)

import numpy as np
# # Plot ACF:
# plt.subplot(121)
# plt.plot(lag_acf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(diff1)), linestyle='--', color='gray')
# plt.axhline(y=1.96/np.sqrt(len(diff1)), linestyle='--', color='gray')
# plt.title('Autocorrelation Function')
#
# # Plot PACF:
# plt.subplot(122)
# plt.plot(lag_pacf)
# plt.axhline(y=0, linestyle='--', color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(diff1)), linestyle='--', color='gray')
# plt.axhline(y=1.96/np.sqrt(len(diff1)), linestyle='--', color='gray')
# plt.title('Partial Autocorrelation Function')
# plt.tight_layout()
# plt.show()
# pd.plotting.autocorrelation_plot(diff1)
# plt.show()

# stats.graphics.plot_acf(diff1)
# plt.show()
# stats.graphics.plot_pacf(diff1)
# plt.show()

print(stats.tsa.stattools.kpss(commits_series))
print(stats.tsa.stattools.kpss(diff1))

# model = stats.tsa.ARIMA(diff1, order=(2, 1, 0))
# results_AR = model.fit(disp=-1)
# plt.plot(diff1)
# plt.plot(results_AR.fittedvalues, color='red')
# plt.title('RSS: %.4f' % np.sum((results_AR.fittedvalues-diff1)**2))
# plt.show()

import itertools
# res_aic = []
# res_bic = []
# for p, q in itertools.product(range(0, 5), range(0, 5)):
#     try:
#         model = stats.tsa.ARIMA(commits_series, order=(p, 1, q))
#         results = model.fit(disp=False)
#         # rss = np.sum((results.fittedvalues - commits_series)**2)
#         res_aic.append((results.aic, (p, q)))
#         res_bic.append((results.bic, (p, q)))
#     except:
#         continue
#
# print(sorted(res_aic))
# print(sorted(res_bic))

results = stats.tsa.ARIMA(commits_series, order=(2, 1, 3)).fit(disp=False)
print(results.summary())
# results.plot_diagnostics(figsize=(15, 12))
# plt.show()

