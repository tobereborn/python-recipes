# -*- coding: utf-8 -*-

# import getData as GD
import pandas as pd
import os
from model import backTestFramework as BT


def readFile(filePath, headerNum=0, indexNum=0):
    """
        读取时间序列数据
    """
    if not os.path.exists(filePath):
        raise IOError("{0} not exists!".format(filePath))
    content_df = pd.read_csv(filePath, header=headerNum, index_col=indexNum)
    content_df.index = pd.to_datetime(content_df.index)
    return content_df


"""
bondDict = {'165509.OF': '信诚增强收益债券(LOF)',
            '090002.OF': '大成债券-A/B',
            '161216.OF': '国投瑞银双债增利债券A'}

stockDict = {'050002.OF': '博时裕富沪深300指数',
             '165511.OF': '信诚中证500指数',
             '159915.OF': '易方达创业板ETF'}

otherDict = {'000217.OF': '华安黄金易ETF联接C',
             '162411.OF': '华宝标普石油指数',
             '096001.OF': '大成标普500',
             '000071.OF': '华夏恒生ETF联接'}

startDate = '2012-01-01'
endDate = '2016-11-30'
combFunc = lambda x, y: x+','+y

bondData = GD.getHistData(reduce(combFunc, bondDict.keys()), startDate, endDate)
stockData = GD.getHistData(reduce(combFunc, stockDict.keys()), startDate, endDate)
otherData = GD.getHistData(reduce(combFunc, otherDict.keys()), startDate, endDate)
"""
bondData = readFile('bondData.txt')
stockData = readFile('stockData.txt')
otherData = readFile('otherData.txt')
"""
# 无约束 不限制大类资产
strategyLow0 = BT.BackTest(netValue=bondData, method='MVO')
yeildLow0, weightsLow0, efPointLow0 = strategyLow0.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                    adjustFreq='1Y', histLength='3Y', show=False)

strategyMid0 = BT.BackTest(netValue=pd.concat([bondData, stockData]), method='MVO')
yeildMid0, weightsMid0, efPointMid0 = strategyMid0.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                    adjustFreq='1Y', histLength='3Y', show=False)

strategyHigh0 = BT.BackTest(netValue=pd.concat([bondData, stockData, otherData]), method='MVO')
yeildHigh0, weightsHigh0, efPointHigh0 = strategyHigh0.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                        adjustFreq='1Y', histLength='3Y', show=False)

# 无约束 限制大类占比
strategyLow = BT.BackTest(netValue=bondData, method='MVO')
yeildLow, weightsLow, efPointLow = strategyLow.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                adjustFreq='1Y', histLength='3Y', show=False)

strategyMid = BT.BackTest(netValue=pd.concat([bondData, stockData]), method='MVO')
factorMatrixMid, boundMid = strategyMid.setInequConstraint(Const1=(['165509.OF', '090002.OF', '161216.OF'], 0.7, 0.7),
                                                           Const2=(['050002.OF', '165511.OF', '159915.OF'], 0.3, 0.3))
yeildMid, weightsMid, efPointMid = strategyMid.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                adjustFreq='1Y', histLength='3Y', show=False,
                                                                factorMatrix=factorMatrixMid, bound=boundMid)

strategyHigh = BT.BackTest(netValue=pd.concat([bondData, stockData, otherData]), method='MVO')
factorMatrixHigh, boundHigh = strategyHigh.setInequConstraint(Const1=(['165509.OF', '090002.OF', '161216.OF'], 0.5, 0.5),
                                                              Const2=(['050002.OF', '165511.OF', '159915.OF'], 0.4, 0.4),
                                                              Const3=(['000217.OF', '162411.OF', '096001.OF', '000071.OF'], 0.1, 0.1))
yeildHigh, weightsHigh, efPointHigh = strategyHigh.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                                    adjustFreq='1Y', histLength='3Y', show=False,
                                                                    factorMatrix=factorMatrixHigh, bound=boundHigh)
"""

# 有约束 限制大类占比 3年历史做未来预计


histLength = '1Y'

# 9-1
strategy9 = BT.BackTest(netValue=pd.concat([bondData, stockData], axis=1), method='MVO')
factorMatrix9, bound9 = strategy9.setInequConstraint(bond1=('165509.OF', 0.7, 0.1), bond2=('090002.OF', 0.7, 0.1),
                                                     bond3=('161216.OF', 0.7, 0.1),
                                                     stock1=('050002.OF', 0.08, 0.01), stock2=('165511.OF', 0.08, 0.01),
                                                     stock3=('159915.OF', 0.08, 0.01),
                                                     Const1=(['165509.OF', '090002.OF', '161216.OF'], 0.9, 0.9),
                                                     Const2=(['050002.OF', '165511.OF', '159915.OF'], 0.1, 0.1))
yeild9, weights9, efPoint9 = strategy9.strategyBackTest(startDate='2015-12-01', endDate='2016-11-30',
                                                        adjustFreq='3M', histLength=histLength, show=True, write=True,
                                                        epsinon=0.001,
                                                        factorMatrix=factorMatrix9, bound=bound9)
