# -*- coding: utf-8 -*-

"""
    This script is used for backtesting
    author: jacobliang
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
import os
import math
import matplotlib.pyplot as plt
import operator
from functools import reduce


class BackTest(object):
    def __init__(self, netValue=None, netValueFile=None, method='MVO', capitalWeights=None, dataFreq='M'):
        """
            初始参数净值和数据频率类型
            netValue, 资产净值时间序列(日粒度)
            dataFreq, 重采样频率，默认转换为月
            netValueFile, 资产净值文件名
        """
        if (netValue is None) == (netValueFile is None):
            raise ValueError("Only Need One between netValue and netValueFile")
        if netValue is not None:
            self.netValue = netValue
        elif netValueFile is not None:
            self._checkFile(netValueFile)
            tmpDF = pd.read_csv(netValueFile, index_col=0)
            tmpDF.index = pd.to_datetime(tmpDF.index)
            self.netValue = tmpDF
        else:
            raise ValueError("Please Supply Net Value Or Net Value File")

        # 初始化净值数据和资产信息
        self._checkValid(method.upper(), ['MVO', 'BL'], 'Method')
        self.method = method.upper()
        if self.method == 'BL':
            if capitalWeights is None:
                raise Exception("If Method is {}, Capital Weights Should be offered".format(method))
            self.capitalWeights = capitalWeights
        self.assetsList = self.netValue.columns
        # 输出读取数据信息
        self.printNetValueInfo()

        # 获取日收益、数据频率标签
        self.dailyReturn = self._getYield(self.netValue)
        self._checkType(dataFreq, str, "Data Frequency")
        self._checkFreq(dataFreq, "Data Frequency")
        self.dataFreq = dataFreq.upper()
        # 根据频率重采样，并计算收益率
        self.yearlyYield = self._getYield(self.netValue.resample(self.dataFreq).first())
        # 数据年化系数
        self.factor = self._comfirmNetValueFreq(dataFreq)
        # 初始化约束
        self.factorMatrix = None
        self.bound = None

    def _checkFile(self, filePath):
        """
            检查文件路径的有效性
            Input Parameter:
                filePath,   路径
            Return:
                Boolen,     路径是否有效
        """
        if not os.path.exists(filePath):
            raise IOError("{} not exists".format(filePath))
        if not filePath.endswith('.txt') and not filePath.endswith('.csv'):
            raise TypeError("{} should be csv or txt".format(filePath))
        return True

    def _checkType(self, var, tagType, varName):
        """
            检查数据类型的有效性
            Input Parameter:
                var,        待检查变量
                tagType,    期望变量类型
            Return:
                boolen,     变量类型与期望类型是否一致
        """
        if not isinstance(varName, str):
            raise TypeError("{} should be Str type".format(varName))
        if not isinstance(var, tagType):
            raise TypeError("{} should be {}".format(varName, tagType))
        return True

    def _checkFreq(self, freq, freqName='Frequency'):
        """
            检查数据频率的有效性
            Input Parameter:
                freq,       频率参数，字符类型
                freqname,   异常辅助说明参数
            Return:
                boolen,     数据频率是否满足预期
        """
        if freq.upper() not in ['D', 'W', 'M', 'Q', 'Y']:
            raise ValueError("{} must be one of ['D', 'W', 'M', 'Q', 'Y']".format(freqName))
        return True

    def _checkValid(self, var, validList, varName='Parameters'):
        """
            检查变量是否满足限定要求
            Input Parameter:
                var,        待检查变量
                validlist,  变量限定列表
            Return:
                boolen,     是否满足限定列表的要求
        """
        if not isinstance(varName, str):
            raise TypeError("The Third Parameter Should be Str")
        if not isinstance(validList, type([])):
            raise TypeError("validList should be type of list")
        if var not in validList:
            raise ValueError("{} should be in {}".format(varName, validList))
        return True

    def _getYield(self, netValue):
        """
            日收益率计算
            Input Parameter:
                value,  净值序列
            Return:
                日收益序列
        """
        return netValue.pct_change().fillna(0)

    def _getAccumulativeReturn(self, value):
        """
            由日收益计算累计收益率
            Input Parameter:
                value,  日收益序列
            Return:
                累计收益序列
        """
        return (1 + value).cumprod() - 1

    def _comfirmNetValueFreq(self, dataFreq):
        """
            返回对应数据频率所对映的交易日数量
            Input Parameter:
                dataFreq,   数据频率
            Return:
                与数据频率想对映的交易日天数, Int类型
        """
        factorDict = {'D': 252, 'W': 52, 'M': 12, 'Q': 4, 'Y': 1}
        return factorDict[dataFreq.upper()]

    def printNetValueInfo(self):
        """
            回测类辅助功能，输出回测数据的相关基本信息
            Input Parameter:
                None
            Return:
                None
        """
        dataPointNum, assetsNum = self.netValue.shape
        columns = self.netValue.columns
        self.netValueStartDate = min(self.netValue.index).date().strftime('%Y-%m-%d')
        self.netValueEndDate = max(self.netValue.index).date().strftime('%Y-%m-%d')
        dataFrequency = self.netValue.index.freq
        print("\n\t\t\t---*--- INPUT DATA INFORMATION ---*---\n")
        print("\tBacktest Method: {}\n".format(self.method))
        print("\tColumn Names: {}\n".format(reduce(lambda x, y: x + ', ' + y, columns)))
        print("\tStart Date: {}\tEnd Date: {}\tFrequency: {}\n".format(self.netValueStartDate,
                                                                       self.netValueEndDate, dataFrequency))
        print("\tData Number: {}\tColumns Number: {}\n".format(dataPointNum, assetsNum))
        if self.method == 'BL':
            rptStartDate = min(self.capitalWeights.index).date().strftime('%Y-%m-%d')
            rptEndDate = max(self.capitalWeights.index).date().strftime('%Y-%m-%d')
            print("\tFund Reports Range: {} --> {}\n".format(rptStartDate, rptEndDate))
            print("\tFund Reports Number: {}\n".format(self.capitalWeights.shape[0]))

    def setInequConstraint(self, upBound=1.0, lowBound=0.0, **kwargs):
        """
            设置权重上下界约束
            Input Parameter:
                upBound,    约束上界，float类型，默认1.0
                lowBound,   约束下界，float类型，默认0.0
                **kwargs
                    针对某一基金设定特定的上下限
                        key-资产代码，为fundlist中的元素
                        value-上下界，tuple类型，输入上下界即可
                    针对某一些基金设置特定的约束
            Return:
                FactorMatrix,   约束所对应的系数矩阵
                bound,          约束所对应的上下界
        """
        fundList = list(self.netValue.columns)
        if not isinstance(upBound, float):
            raise TypeError("upBound must be float")
        if not isinstance(lowBound, float):
            raise TypeError("lowBound must be float")
        if operator.le(upBound, lowBound):
            raise ValueError("UpBound must be greater than lowBound")
        if operator.gt(upBound, 1.0):
            raise ValueError("UpBound must be less than 1")
        if operator.gt(0.0, lowBound):
            raise ValueError("lowBound must be greater than 0.0")
        fundCnt = len(fundList)
        upFactorMatrix = np.eye(fundCnt)
        lowFactorMatrix = np.eye(fundCnt) * -1.0
        factorMatrix = np.vstack((upFactorMatrix, lowFactorMatrix))
        boundUp = np.ones((fundCnt, 1)) * min(upBound, 1.0)
        boundLow = np.ones((fundCnt, 1)) * max(lowBound, 0.0) * -1.0
        bound = np.vstack((boundUp, boundLow))
        # 添加特定维度的特殊约束
        if len(kwargs) > 0:
            factorArray, boundArray = self._generateUnequalConstraint(bound, kwargs)
            factorMatrix = np.vstack((factorMatrix, factorArray))
            bound = np.vstack((bound, boundArray))
        # 返回不等式约束
        return factorMatrix, bound

    def _generateUnequalConstraint(self, selfBound, kwargs):
        """
            处理约束问题中的特殊组合约束，self.setInequConstraint调用函数
            Input Parameter:
                selfBound,  构建的基本约束界限向量
                kwargs,     特殊组合约束
            Return:
                retfactor,  增量系数矩阵
                retbound,   增量界限向量
        """
        fundList = list(self.netValue.columns)
        fundCnt = len(fundList)
        retfactor = list()
        retBound = list()
        for val in kwargs.values():
            if len(val) != 3:
                raise ValueError("There should be fundCode, upbound and lowBound")
            if isinstance(val[0], type([])):
                # 构建系数举证 上下界
                factorArray = np.zeros((2, len(fundList)))
                boundArray = np.vstack((np.ones((1, 1)), np.zeros((1, 1))))
                for elem in val[0]:
                    factorArray[0][fundList.index(elem)] = 1.0
                    factorArray[1][fundList.index(elem)] = -1.0

                # 构建上下约束值
                if operator.gt(max(val[1:]), 1.0):
                    raise ValueError("{0}'s up bound should not be greater than 1.0".format(val[0]))
                if operator.gt(0.0, min(val[1:])):
                    raise ValueError("{0}'s low bound should not be less than 0.0".format(val[0]))
                if self._checkType(max(val[1:]), float, 'Upbound'):
                    boundArray[0][0] = max(val[1:])
                if self._checkType(min(val[1:]), float, 'LowBound'):
                    boundArray[1][0] = min(val[1:]) * -1.0
                # 将系数及约束添加至结果表
                retfactor.append(factorArray)
                retBound.append(boundArray)
            else:
                fundIndex = fundList.index(val[0])
                if operator.gt(max(val[1:]), 1.0):
                    raise ValueError("{0}'s up bound should not be greater than 1.0".format(val[0]))
                if operator.gt(0.0, min(val[1:])):
                    raise ValueError("{0}'s low bound should not be less than 0.0".format(val[0]))
                if self._checkType(max(val[1:]), float, 'Upbound'):
                    selfBound[fundIndex][0] = max(val[1:])
                if self._checkType(min(val[1:]), float, 'LowBound'):
                    selfBound[fundIndex + fundCnt][0] = min(val[1:]) * -1.0
        return np.vstack(retfactor), np.vstack(retBound)

    def _getTargetWeight(self, weights, ras, tag=None):
        """
            获取特定风险厌恶系数所对映的组合，默认取中值
            Input Parameter:
                weights,    待抽取组合权重序列
                ras,        对映风险厌恶序列
                tag,        厌恶系数标的
            Return:
                对映权重向量
        """

        def getIndex(dataList, tag):
            if not isinstance(tag, type(dataList[0])):
                raise TypeError("{} should be type of {}".format(tag, type(dataList[0])))
            tagValue = dataList[0]
            gap = math.fabs(dataList[0] - tag)
            for data in dataList:
                if operator.lt(math.fabs(data - tag), gap):
                    gap = math.fabs(data - tag)
                    tagValue = data
            return dataList.index(tagValue)

        tagIndex = int()
        if tag is None:
            tagIndex = getIndex(ras, (max(ras) + min(ras)) / 2.0)
            # tagIndex = Npts//2.0
        else:
            tagIndex = getIndex(ras, tag)

        return weights[tagIndex]

    def _return_covariance(self, return_df, factor):
        """
            计算收益率的平均年化收益、年化协方差，年化
            Input Parameter:
                return_df,  日收益序列，DataFrame类型
                factor,     年化系数
            Return:
                ExpReturn,  预期收益
                ExpCov,     预期协方差
                Sigma,      资产波动
        """
        ExpReturn = return_df.mean().apply(lambda x: (1 + x) ** factor - 1)
        Sigma = np.matrix(return_df.std().apply(lambda x: x * np.sqrt(factor)))
        ExpCov = return_df.cov() * factor
        return ExpReturn, ExpCov, Sigma

    def computePortfolio(self, ExpReturn, ExpCov, factorMatrix=None, bound=None, Npts=1000, delta=10,
                         epsinon=0.0001):
        """
            有效前沿计算函数，MVO计算方法
            Input Parameter:
                ExpReturn,      资产预期收益，DataFrame类型
                ExpCov,         资产预期协方差系数举证，DataFrame类型
                factorMatrix,   组合约束系数矩阵，ndarray类型，默认None
                bound,          组合约束上下界向量，ndarray类型，默认None
                Npts,           有效前沿初始点数，Int类型，默认1000
                delta,          有效前沿风险厌恶系数搜索步长，Int类型，默认10
                epsinon,        有效前沿比较精度，浮点型，默认1e-4
            Return:
                risks,          有效前沿风险序列
                returns,        有效前沿收益序列
                riskAversions,  有效前沿对映风险厌恶序列
                weights,        与有效前沿相对应的组合序列
        """
        from model import MVO
        mvo = MVO.Markowitz(np.matrix(ExpReturn), np.matrix(ExpCov))
        if (factorMatrix is None) != (bound is None):
            raise ValueError("FactorMatrix must be corresponding to bound")
        if factorMatrix is None or bound is None:
            print(">>> Compute Unconstraint Portfolio")
            factorMatrix, bound = self.setInequConstraint(1.0, 0.0)
            risks, returns, riskAversions, weights = mvo.constraint_frontier(factorMatrix, bound,
                                                                             Npts, delta, epsinon)
        else:
            print(">>> Compute Constraint Portfolio")
            risks, returns, riskAversions, weights = mvo.constraint_frontier(factorMatrix, bound,
                                                                             Npts, delta, epsinon)
        return risks, returns, riskAversions, weights

    def generateDefaultViews(self):
        """
            构建默认的Views, P Q 全部为0，置信度为100%
            Input Parameter:
                None
            Return:
                对映资产矩阵，对映观点矩阵，对映置信度
        """
        default_P = np.zeros(len(self.assetsList))
        default_Q = np.zeros(1)
        # 将置信度默认设置为100%
        default_Conf = 1.0
        return np.array([default_P]), np.array([default_Q]), [default_Conf]

    def getCapitalWeights(self, startDate, endDate):
        """
            获取计算区间的资本占比
            Input Parameter:
                startDate,  开始日期
                endDate,    结束日期
            Return:
                区间基金资产净值比
                区间末报告日期，datetime
        """

        def getWeightPct(value_df):
            return value_df.apply(lambda x: [elem / sum(x) for elem in x], axis=1)

        #  确保每一列为一个百分比组合
        capitalWeightsDF = getWeightPct(self.capitalWeights)
        # return capitalWeightsDF[startDate:endDate]
        return capitalWeightsDF[startDate:endDate].values[-1], max(capitalWeightsDF[startDate:endDate].index)

    def computeBL(self, Cov, weq, P=None, Q=None, Conf=None, tau=0.05, delta=3.07):
        """
            BL调用计算函数
            Input Parameter:
                Cov,    历史协方差矩阵
                weq,    资产历史市值
                P,      预期观点资产涉及矩阵
                Q,      预期观点资产收益变动幅度矩阵
                Conf,   预期观点置信度矩阵
                tau,    风险厌恶系数
                delta,
            Return:
                PostReturn, 平均收益的后验估计
                EquWeights, 给定后验平均收益及方差时的，无约束资产配比
                ViewImpact, view对对后验平均收益的影响水平
        """
        from model import BlackLitterman as BL
        # P和Q必须同时输入或都不输入
        if (P is None) != (Q is None):
            raise ValueError("P and Q should be one-to-one corresponding relations")

        if P is not None and Conf is not None:
            if len(P) != len(Q):
                raise ValueError("P and Q should be one-to-one corresponding relations")
            if len(P) != len(Conf):
                raise ValueError("View and Confidence should be one-to-one corresponding ralation")
        elif P is not None and Conf is None:
            Conf = self.generateDefaultViews()[2]
        elif P is None and Conf is None:
            P, Q, Conf = self.generateDefaultViews()
        else:
            raise Exception("Parameters Error, There is Conf but no View")

        if isinstance(Cov, DataFrame):
            Cov = Cov.values
        # 参数准备计算
        tauCov = Cov * tau
        Omega = np.dot(np.dot(P, tauCov), P.T)
        BLmodel = BL.BlackLitterman(weq=weq, sigma=Cov, P=P, Q=Q, Omega=Omega, tau=tau, delta=delta)
        # PostReturn, EquWeights, ViewImpact = BLmodel.compute_idz_ER(Conf)
        if np.all(P == 0.0):
            PostReturn = BLmodel.computePi()
            return (PostReturn,)
        else:
            PostReturn, EquWeights, ViewImpact = BLmodel.compute_idz_ER(Conf)
            return PostReturn, EquWeights, ViewImpact

    def splitDateChunk(self, startDate, endDate, adjustFreq='Q'):
        """
            按照回测区间和调整频率，返回时间序列切片列表
            Input Parameter:
                startDate,      开始日期
                endDate,        结束日期
                adjustFreq,     调整频率
            Return:
                retList,        按频率分块的时间标签序列
        """
        self._checkType(adjustFreq, str, 'adjustFreq')
        adjustFreq = adjustFreq.upper()
        freqDict = {'1M': 1, '3M': 3, '6M': 6, '9M': 9, '12M': 12, '1Y': 12, 'Y': 12,
                    '1Q': 3, 'Q': 3, '2Q': 6, '3Q': 9}

        if adjustFreq not in freqDict.keys():
            raise ValueError("Frequency should be one of {}".format(freqDict.keys()))

        aimDateRange = sorted(list(set(map(lambda x: x.strftime("%Y-%m"),
                                           self.yearlyYield[startDate:endDate].index))))
        totalMonthNum = len(aimDateRange)
        if freqDict[adjustFreq] > totalMonthNum:
            raise Exception("Frequency is out of aim date range")

        retList = list()
        for index in range(int(math.ceil(float(totalMonthNum) / float(freqDict[adjustFreq])))):
            startPoint = index * freqDict[adjustFreq]
            if (index + 1) * freqDict[adjustFreq] - 1 >= totalMonthNum:
                endPoint = totalMonthNum - 1
            else:
                endPoint = (index + 1) * freqDict[adjustFreq] - 1
            # endPoint = (index+1)*freqDict[adjustFreq]-1
            retList.append((aimDateRange[startPoint], aimDateRange[endPoint]))
        return retList

    def getHistChunk(self, startDate, histLength):
        """
            按histLength取历史长度数据, 子块按月划分
            Input Parameter:
                startDate,      开始日期
                histLength,     历史长度
            Return:
                histStartDate,  符合长度要求的历史数据开始日期
                histEndDate,    符合长度要求的历史数据结束日期
        """
        self._checkType(histLength, str, 'histLength')
        histLength = histLength.upper()

        lengthDict = {'1Y': 1, '2Y': 2, '3Y': 3, '4Y': 4, '5Y': 5, '7Y': 7, '9Y': 9}
        if histLength not in lengthDict.keys():
            raise Exception("The Range should be in {}".format(lengthDict.keys()))

        from dateutil.parser import parse
        from datetime import timedelta
        histTimpStamp = parse(startDate) - timedelta(1)
        histEndDate = histTimpStamp.strftime("%Y-%m-%d")
        histStartDate = (histTimpStamp - timedelta(lengthDict[histLength] * 365)).strftime("%Y-%m-%d")
        if histTimpStamp - timedelta(lengthDict[histLength] * 365) < min(self.netValue.index):
            print("There is not enough data for training!")
        return histStartDate, histEndDate

    def strategyBackTest(self, startDate, endDate, adjustFreq, histLength,
                         factorMatrix=None, bound=None, tag=None, Npts=1000, searchDelta=10, epsinon=0.0001,
                         P=None, Q=None, Conf=None, tau=0.05, delta=3.07,
                         write=True, show=True, **karg):
        """
            策略回测
            Input Parameter:
                startDate,      回测开始日期
                endDate,        回测结束日期
                adjustFreq,     回测区间的组合调整周期长度
                histLength,     回测回溯历史长度
                factorMatrix,   约束系数矩阵
                bound,          约束上下界向量
                tag,            厌恶系数标的
                Npts,           前沿点数量
                searchDelta,    搜索前沿风险最小点的搜索步长
                epsinon,        搜索前沿的停止精度
                P,              Views矩阵
                Q,              与View矩阵对映的涨跌幅矩阵
                Conf,           Views对映的置信度
                tau,            BL模型参数
                delta,          BL模型参数
                write,          是否将结果写出, True/False
                show,           是否展示图示, True/False
                **karg
            Return：
                portfolioAccumulateYield,   组合累计收益序列
                adjustWeights,              多次调整权重序列
                diffEFChunkList,            前沿曲线
        """
        if (factorMatrix is None) != (bound is None):
            raise ValueError("FactorMatrix and bound should be one-to-one corresponding relations")
        # if factorMatrix is None:
        #     factorMatrix = self.factorMatrix
        #     bound = self.bound
        adjustFreqList = self.splitDateChunk(startDate, endDate, adjustFreq)
        # 组合日净值列表
        portNetValueList = list()
        # 选定权重列表
        weightsList = list()
        # 前沿对映权重存储列表
        diffEFChunkWeightsList = list()
        # 前沿对映存储列表
        diffEFChunkList = list()
        for anchor in adjustFreqList:
            print("--*-- Assets Allocation Time: {} --*--".format(adjustFreqList.index(anchor)))

            # 锚定测试区间和历史数据区间
            # backTestingData = self.dailyReturn[anchor[0]:anchor[1]]
            backTestingData = self.netValue[anchor[0]:anchor[1]]
            backTestMinDate = min(backTestingData.index).strftime("%Y-%m-%d")
            backTestMaxDate = max(backTestingData.index).strftime("%Y-%m-%d")

            # 确定测试数据和历史参考数据
            histStartDate, histEndDate = self.getHistChunk(backTestMinDate, histLength)
            trainingData = self.yearlyYield[histStartDate:histEndDate]

            # 输出每次调整的时间范围
            print("Allocative Range: {} --> {}".format(anchor[0], anchor[1]))
            print("BackTest StartDate: {} --> EndDate: {}".format(backTestMinDate, backTestMaxDate))
            print("BackTest Data Points Number: {}".format(backTestingData.shape[0]))
            print("Histical Data Range: {} --> {}".format(histStartDate, histEndDate))
            print("Histical Data Points Number: {}".format(trainingData.shape[0]))

            # MVO标准参数计算
            # expReturn, expCov, expSigma = self._return_covariance(trainingData, self.factor)
            PriorReturn, PriorCov, PriorSigma = self._return_covariance(trainingData, self.factor)
            print('trainingData:')
            print(trainingData)
            print('PriorReturn:')
            print(PriorReturn)
            print('PriorCov:')
            print(PriorCov)
            print('PriorSigma:')
            print(PriorSigma)
            if self.method == 'BL':
                # 获取当前区间的基金资产净值比及基金报告日期
                PeriodCapitalWeights, rptDate = self.getCapitalWeights(histStartDate, histEndDate)
                print("The Capital Allocation Report Date is: {}".format(rptDate.strftime('%Y-%m-%d')))
                print("Capital Allocations: {}".format(PeriodCapitalWeights))
                # 计算市场均衡收益
                PosteriorResult = self.computeBL(PriorCov, PeriodCapitalWeights, P, Q, Conf)
                PosteriorReturn = PosteriorResult[0]
                # 检测结果
                print("Posterior Return is: {}".format(PosteriorReturn))
                PriorReturn = PosteriorReturn
                print("Replacing Prior Return With Posterior Return!")
            # 约束检查
            # portRisks, portReturns, portWeights = self.computePortfolio(expReturn, expCov,
            #                                                             self.factorMatrix, self.bound, Npts)
            print('factorMatrix:')
            print(factorMatrix)
            print('bound:')
            print(bound)
            portRisks, portReturns, portRAs, portWeights = self.computePortfolio(PriorReturn, PriorCov,
                                                                                 factorMatrix, bound,
                                                                                 Npts, searchDelta, epsinon)
            print('portRisks:')
            print(portRisks)
            print('portReturns:')
            print(portReturns)
            print('portRAs:')
            print(portRAs)
            print('portWeights:')
            print(portWeights)
            print("Optimal Computation Finished!")
            # 构造前沿DataFrame（三维结果）
            efPoints = DataFrame({'Risks': portRisks, 'Returns': portReturns, 'RiskAversions': portRAs})
            print('efPoints:')
            print(efPoints)
            # 构造前沿对映的权重DataFrame
            efWeights = DataFrame(portWeights, columns=self.assetsList)
            print('efWeights:')
            print(efWeights)
            # 选取特定组合权重
            midRiskWeights = self._getTargetWeight(portWeights, portRAs)
            print('midRiskWeights:')
            print(midRiskWeights)
            # 将选取的权重构造成DataFrame
            midRiskWeightsDF = DataFrame(np.array(midRiskWeights).T, columns=self.assetsList)
            print('midRiskWeightsDF:')
            print(midRiskWeightsDF)

            # 由日收益块构造组合日收益DataFrame  修改为
            # 组合收益的计算方法进行调整
            # 由每日净值进行组合-->计算组合的日收益-->计算组合的累计收益-->返回组合的日净值
            # 组合净值
            portNetValue = backTestingData.dot(midRiskWeights)
            portNetValue.columns = ['PortfolioNetValue']
            # portfolioYield = backTestingData.dot(midRiskWeights)
            # portfolioYield.columns = ['Portfolio']
            print("Portfolio Computation Finished!")
            # 添加每一频次计算结果
            diffEFChunkList.append(efPoints)
            diffEFChunkWeightsList.append(efWeights)
            weightsList.append(midRiskWeightsDF)
            portNetValueList.append(portNetValue)
            print("Collected Sub_Results Finished!\n")

        # 频次调整权重变化组合成
        adjustWeights = pd.concat(weightsList)
        adjustWeights.index = range(adjustWeights.shape[0])
        # 组合日净值DataFrame
        portfolioDailyNetValue = pd.concat(portNetValueList)
        portfolioDailyYield = self._getYield(portfolioDailyNetValue)
        portfolioDailyYield.columns = ['PortfolioDailyYield']
        # 组合累计收益率DataFrame
        portfolioAccumulateYield = self._getAccumulativeReturn(portfolioDailyYield)
        portfolioAccumulateYield.columns = ['PortfolioAccumulatedYield']

        if write is True:
            # 输出每一频次调整的权重变化
            adjustWeights.to_csv("adjustWeights.txt", encoding='utf-8')
            # 输出组合日收益
            portfolioDailyYield.to_csv("portfolioDailyYield.txt", encoding='utf-8')
            # 输出组合累计收益
            portfolioAccumulateYield.to_csv("AccumPortYield.txt", encoding='utf-8')
            for index in range(len(diffEFChunkList)):
                diffEFChunkList[index].to_csv("Efficient_frontier_%s.txt" % index, encoding='utf-8')
            for index in range(len(diffEFChunkWeightsList)):
                diffEFChunkWeightsList[index].to_csv("Efficient_frontier_weights_%s.txt" % index, encoding='utf-8')
            print("All The Result Writed down Successfully!")

        if show is True:
            self._reusltSummary(portfolioAccumulateYield, adjustWeights, diffEFChunkList, diffEFChunkWeightsList)
        return portfolioAccumulateYield, adjustWeights, diffEFChunkList

    def _reusltSummary(self, accumYield=None, weightsTendency=None, diffEFList=None, diffEFWeightsList=None):
        """
            组合结果图表展示
            单次调整，展示前沿及累计面积图
            多次调整展示累计收益和每次权重变化
        """
        if (accumYield is None) and (weightsTendency is None) \
                and (diffEFList is None) and (diffEFWeightsList is None):
            raise Exception("There should be (accumYield, weightsTendency) or (diffEFList, diffEFWeightsList)")
        figSummary = plt.figure()
        ax1 = figSummary.add_subplot(2, 1, 1)
        ax2 = figSummary.add_subplot(2, 1, 2)
        # ax2为百分比累计面积图，限制Y轴范围
        ax2.set_ylim([0.0, 1.0])
        if len(diffEFList) == 1 and len(diffEFWeightsList) == 1:
            # 一次调整，画前沿和累计面积百分比
            diffEFList[0].plot.scatter(x='Risks', y='Returns', ax=ax1)
            diffEFWeightsList[0][::-1].plot.area(ax=ax2)
            self.plot3DEF(diffEFList[0]['Risks'], diffEFList[0]['Returns'], diffEFList[0]['RiskAversions'])
        elif (accumYield is not None) and (weightsTendency is not None):
            # 多次调整，画累计前沿和调整权重变化趋势
            accumYield.plot(ax=ax1)
            weightsTendency.plot.area(ax=ax2)
        else:
            pass
        plt.show()

    def plot3DEF(self, ef_risks, ef_returns, ef_ras):
        """
            绘制前沿及风险厌恶的3D图
            ef_risks,   前沿波动--X轴
            ef_returns, 前沿收益--Y轴
            ef_ras,     前沿风险厌恶系数--Z轴
        """
        if len(ef_risks) != len(ef_returns):
            raise Exception("The risks and returns should contain the same points")
        from matplotlib import pyplot
        import pylab
        from mpl_toolkits.mplot3d import Axes3D
        fig = pylab.figure()
        ax = Axes3D(fig)
        ax.scatter(ef_risks, ef_returns, ef_ras)
        pyplot.show()
