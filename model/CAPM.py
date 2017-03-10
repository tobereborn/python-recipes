# -*- coding: utf-8 -*-

"""
    This script is used for computing CAPM model to evaluate a portfolio
    @author: jacobliang
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
from numpy.lib.stride_tricks import as_strided
import statsmodels.api as sm
from math import sqrt
import operator


class CAPM(object):
    """
        CAPM Model
        计算组合绩效指标
        Input Parameter:
            R_P: DataFrame 组合日净值
            R_M: DataFrame 市场日净值
            R_F: DataFrame 无风险日收益率
    """

    def __init__(self, R_P, R_M, R_F=None, RF_totalYield=None, dataFreq='D'):
        if not isinstance(R_P, DataFrame):
            raise TypeError("R_P must be DataFrame")
        if not isinstance(R_M, DataFrame):
            raise TypeError("R_M must be DataFrame")
        if operator.gt(R_P.shape[0], R_M.shape[0]):
            raise ValueError("BenchMark should have more data points")
        if R_F is None:
            if RF_totalYield is None:
                raise ValueError("There must be risk free related input")
            else:
                if not isinstance(RF_totalYield, float):
                    raise ValueError("RF_totalYield must be type float")
                R_F = self.generateYieldSeries(RF_totalYield, R_P.index)
        elif not isinstance(R_M, DataFrame):
            raise TypeError("R_F must be DataFrame")
        else:
            pass

        # data_df = pd.concat([R_P, R_M, R_F], axis=1)
        # self.data = data_df.dropna()
        # 组合原始净值
        self.originalNetValue = R_P
        # 组合日收益
        self.R_P = R_P.pct_change().fillna(0)
        # 市场标的日收益
        self.R_M = R_M[min(R_P.index):max(R_P.index)].pct_change().fillna(0)
        # 无风险日收益
        self.R_F = R_F

        # 组合累计收益序列
        self.AccumulatedYield = self.accumulatedYield()
        # 市场标的相同区间的累计收益率序列
        self.benchmarkAcYield = self.accumulatedYield(self.R_M)
        self.benchmarkAcYield.columns = ['BenchMark']
        # 组合净值
        self.PortfolioNetValue = self.AccumulatedYield + 1.0
        self.PortfolioNetValue.columns = ['Portfolio Net Value']

        self.periodLength = self.R_P.shape[0]
        self.dataFreq, self.dataFactor = self._checkFreq(dataFreq)

    def _checkFreq(self, freq='D', freqName='Frequency'):
        """
            检查并会返回数据频率
        """
        if freq.upper() not in ['D', 'W', 'M', 'Q', 'Y']:
            raise ValueError("{} must be one of ['D', 'W', 'M', 'Q', 'Y']".format(freqName))
        factorDict = {'D': 252, 'W': 52, 'M': 12, 'Q': 4, 'Y': 1}
        return freq.upper(), factorDict[freq.upper()]

    def generateYieldSeries(self, yearlyYield, timeIndex, dataFreq='D', colName='Yield'):
        """
            产生具有特定年化收益的定长日收益序列，假定每日收益相等
        """
        if not isinstance(yearlyYield, float):
            raise TypeError("Yearly Yield must a float")
        factor = float(self._checkFreq(dataFreq)[1])
        period = float(len(timeIndex))
        totalYield = (yearlyYield + 1.0) ** (period / factor) - 1.0
        dailyYield = (totalYield + 1.0) ** (1.0 / period) - 1.0
        return DataFrame({colName: [dailyYield] * int(period)}, index=timeIndex)

    def portfolioYield(self, valuesDF=None):
        """
            年化收益率
            由日收益序列计算年化收益
        """
        if valuesDF is None:
            valuesDF = self.R_P
        # totalYield = reduce(lambda x, y: x*y, valuesDF+1.0)-1.0
        totalYield = self.accumulatedYield(valuesDF).ix[-1, 0]
        yearlyYield = (1.0 + totalYield) ** (float(self.dataFactor) / float(self.periodLength)) - 1.0
        return yearlyYield

    def accumulatedYield(self, valuesDF=None):
        """
            累计收益序列计算
        """
        if valuesDF is None:
            valuesDF = self.R_P
        return (1.0 + valuesDF).cumprod() - 1

    def sharpeRatio(self):
        """
            组合单位风险下的所能获得超额收益的程度
            夏普比率越高代表考虑风险的情况下组合表现越好
        """
        sharpe = (self.portfolioYield(self.R_P) - self.portfolioYield(self.R_F)) / (
        self.R_P.std() * sqrt(self.dataFactor))
        return sharpe[0]

    def infoRatio(self):
        """
            组合相对于某一标的的残差收益的收益风险比。
            信息比率越高，组合在承担单位残差风险的情况下获取的残差收益越高，表现越好
            先求解均值和标准差，再年化求比值
        """
        yearlyMean = (1.0 + (self.R_P.ix[:, 0] - self.R_M.ix[:, 0]).mean()) ** self.dataFactor - 1.0
        yearlyStd = (self.R_P.ix[:, 0] - self.R_M.ix[:, 0]).std() * sqrt(self.dataFactor)
        # return (self.R_P - self.R_M).mean()/(self.R_P - self.R_M).std()
        return yearlyMean / yearlyStd

    def yearlyStd(self):
        """
            组合的年化波动/年化标准差
        """
        return (self.R_P.std() * sqrt(self.dataFactor))[0]

    def beta(self):
        """
            组合与市场走势的相关程度，解释市场收益
        """
        cov = np.cov(self.R_P.ix[:, 0] - self.R_F.ix[:, 0], self.R_M.ix[:, 0] - self.R_F.ix[:, 0])
        return cov[0][1] / cov[1][1]

    def alpha(self):
        """
            市场之外的超额收益
        """
        pass

    def line_regression(self):
        """
            线性拟合参数计算
        """
        x = self.R_M.ix[:, 0] - self.R_F.ix[:, 0]
        Y = self.R_P.ix[:, 0] - self.R_F.ix[:, 0]
        X = sm.add_constant(x)
        model = sm.OLS(Y, X)
        results = model.fit()
        self.OLS_summary = results.summary()
        self.OLS_alpha = results.params[0]
        self.OLS_beta = results.params[1]
        self.OLS_r2 = results.rsquared
        self.OLS_r2_adj = results.rsquared_adj
        self.OLS_std_alpha = results.bse[0]
        self.OLS_std_beta = results.bse[1]
        self.adj_beta_param = 1.0 / 3.0
        self.OLS_adj_beta = self.adj_beta_param + (1 - self.adj_beta_param) * results.params[1]
        resultDict = {"alpha": results.params[0], "beta": results.params[1],
                      "r2": results.rsquared, "r2_adj": results.rsquared_adj,
                      "std_alpha": results.bse[0], "std_beta": results.bse[1],
                      "adj_beta": self.OLS_adj_beta}
        return results.summary(), resultDict

    # Tracking Error指标计算
    def trackingError(self):
        # print "BenchMark is Market Return\n"
        return (self.R_P.ix[:, 0] - self.R_M.ix[:, 0]).std()

    # 滚动回撤调用函数capm
    def max_dd(self, ser):
        max2here = pd.expanding_max(ser)
        dd2here = ser - max2here
        return dd2here.min()

    # Rolling Drawdown和Max Drawdown计算
    def rolling_drawdown(self, window_length=10, min_periods=0):
        rolling_dd = pd.rolling_apply(self.R_P, window_length, self.max_dd, min_periods)
        return rolling_dd, rolling_dd.min()[0]

    # 按窗口大小生成矩阵
    def windowed_view(self, x, window_size):
        """Creat a 2d windowed view of a 1d array.

        `x` must be a 1d numpy array.

        `numpy.lib.stride_tricks.as_strided` is used to create the view.
        The data is not copied.

        Example:

        >>> x = np.array([1, 2, 3, 4, 5, 6])
        >>> windowed_view(x, 3)
        array([[1, 2, 3],
               [2, 3, 4],
               [3, 4, 5],
               [4, 5, 6]])
        """
        y = as_strided(x, shape=(x.size - window_size + 1, window_size),
                       strides=(x.strides[0], x.strides[0]))
        return y

    # rolling_drawdown和Max Drawdown计算方法二
    def rolling_max_dd(self, window_size=10, min_periods=1):
        """Compute the rolling maximum drawdown of `x`.

        `x` must be a 1d numpy array.
        `min_periods` should satisfy `1 <= min_periods <= window_size`.

        Returns an 1d array with length `len(x) - min_periods + 1`.
        """
        x = self.R_P.ix[:, 0]
        if min_periods < window_size:
            pad = np.empty(window_size - min_periods)
            pad.fill(x[0])
            x = np.concatenate((pad, x))
        y = self.windowed_view(x, window_size)
        running_max_y = np.maximum.accumulate(y, axis=1)
        dd = y - running_max_y
        return pd.Series(dd.min(axis=1), index=self.R_P.index), dd.min(axis=1).min()


def evaluate(dataDF, weights, startDate, endDate, benchMark, riskFree=None, freeYield=None, dataFreq='D'):
    """
        组合表现评价函数，模型测试评价入口
        Input parameter:
            dataDF,     资产净值数据，DF类型
            weights,    资产权重，与资产个数对映
            startDate,  组合配置开始日期
            endDate,    组合配置结束日期
            benchMark,  市场标的，DF类型
            riskFree,   无风险收益，DF类型
    """
    portfolio = DataFrame(dataDF[startDate:endDate].dot(weights))
    portfolio.columns = ['Portfolio']
    portWeights = DataFrame(weights, columns=['Weights'], index=dataDF.columns)

    if riskFree is not None:
        capm = CAPM(R_P=portfolio, R_M=benchMark, R_F=riskFree)
    else:
        capm = CAPM(R_P=portfolio, R_M=benchMark, RF_totalYield=freeYield)

    print("\n\t\t--*-- Evaluation Information --*--")
    print("NetValue Range:\t\t{} --> {}".format(min(portfolio.index).strftime("%Y-%m-%d"),
                                                max(portfolio.index).strftime("%Y-%m-%d")))
    print("BenchMark Range:\t{} --> {}".format(min(capm.R_M.index).strftime("%Y-%m-%d"),
                                               max(capm.R_M.index).strftime("%Y-%m-%d")))
    print("RiskFree Range:\t\t{} --> {}".format(min(capm.R_F.index).strftime("%Y-%m-%d"),
                                                max(capm.R_F.index).strftime("%Y-%m-%d")))

    # 回归类指标计算
    regressionSummary, regressionDict = capm.line_regression()
    print("\n\t\t--*-- Regression Evaluation --*--")
    # print regressionSummary
    print("Alpha:\t\t{}\t Beta:\t\t{}".format(regressionDict['alpha'], regressionDict['beta']))
    print("R2:\t\t{}\t Adjust R2:\t{}".format(regressionDict['r2'], regressionDict['r2_adj']))
    print("Std Alpha:\t{}\t Std Beta:\t{}".format(regressionDict['std_alpha'], regressionDict['std_beta']))
    print("Adjust Beta:\t{}".format(regressionDict['adj_beta']))

    # 收益类指标
    yearlyYield = capm.portfolioYield()

    # 累计收益作图数据
    accumulatedYieldCompareDF = pd.concat([capm.AccumulatedYield, capm.benchmarkAcYield], axis=1)
    accumulatedYield = capm.AccumulatedYield.ix[-1, 0]
    print("\n\t\t--*-- Yield Evaluation --*--")
    print("Yearly Yield:\t{}\t Accumulated Yield:\t{}".format(yearlyYield, accumulatedYield))

    # 综合指标计算
    sharpeRatio = capm.sharpeRatio()
    infoRatio = capm.infoRatio()
    print("\n\t\t--*-- Aggregative Evaluation --*--")
    print("Sharpe Ratio:\t{}\t Information Ratio:\t{}".format(sharpeRatio, infoRatio))

    # 风险类指标计算
    # rollingDD, maxDD = capm.rolling_drawdown()
    rollingDD, maxDD = capm.rolling_max_dd()
    trackingError = capm.trackingError()
    yearlyStd = capm.yearlyStd()
    print("\n\t\t--*-- Risk Evaluation --*--")
    print("Yearly Std:\t{}\t Max Drawndown:\t\t{}\nTrackingError:\t{}".format(yearlyStd, maxDD, trackingError))

    # import matplotlib.pyplot as plt
    # figSummary = plt.figure()
    # axList = [figSummary.add_subplot(2, 2, x+1) for x in range(4)]
    # capm.PortfolioNetValue.plot(ax=axList[0])
    # portWeights.plot(kind='pie', subplots=True, ax=axList[2])
    # accumulatedYieldCompareDF.plot(ax=axList[1])
    # DataFrame(rollingDD, columns=['Rolling Drawdown']).plot(ax=axList[3])
    # plt.show()

    import matplotlib.pyplot as plt

    capm.PortfolioNetValue.plot(title=u'Portfolio NetValue')
    portWeights.plot(kind='pie', subplots=True, title=u'Assets Weights', legend=False)
    accumulatedYieldCompareDF.plot(title=u'Portfolio Accumulated Yield')
    DataFrame(rollingDD, columns=['Portfolio Rolling Drawdown']).plot(title=u'Portfolio Rolling Drawdown')
    plt.show()
