# -*- coding:UTF-8 -*-
# !/usr/bin/env python

"""
This code is used for computing efficient frontier
basic code is from 1-mv2.py andrewMa
@author: jacobliang
"""

import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers
import math
import operator


solvers.options['show_progress'] = False


class Markowitz(object):
    #This class is used for computing the markowitz model
    #initial some default parameters
    """
    Markowitz model
    类初始化需要输入预期收益（行矩阵）和资产的协方差矩阵
    Initialize Parameter:
        ExpReturn: 预期收益矩阵，np.matrix类型, 列向量
        ExpCovariance： 基金收益率协方差矩阵
    """
    def __init__(self, ExpReturn, ExpCovariance):
        """
            Initialize Parameter:
                ExpReturn: 预期收益矩阵，np.matrix类型, 列向量
                ExpCovariance： 基金收益率协方差矩阵
        """
        if not self.isSemidefinite(ExpCovariance):
            print("The ExpCovariance is not positive semi-definite, the result may unaccuracy!")
        self.n = ExpReturn.size
        self.ExpReturn = ExpReturn
        self.ExpCovariance = ExpCovariance
        self.weights = np.matrix(1.0/self.n * np.ones(self.n))
        self.S = opt.matrix(ExpCovariance)
        self.G = -opt.matrix(np.eye(self.n))
        self.h = opt.matrix(0.0, (self.n, 1))
        print("Successfully Initialized Markowitz Solver")

    def setInequalityBound(self, factorMatrix, boundVector):
        """
            set inequality bounds
        """
        self.G = opt.matrix(factorMatrix)
        self.h = opt.matrix(boundVector)

    def resetDefaultBound(self):
        """
            set the inequality bounds to default value
        """
        self.G = -opt.matrix(np.eye(self.n))
        self.h = opt.matrix(0.0, (self.n, 1))
        print("Parameters reset done!")

    def isSemidefinite(self, ExpCovariance):
        """
            检查协方差矩阵是否满足半正定
            __init__调用内部方法
        """
        eigenvalueList = np.linalg.eigvals(ExpCovariance)
        #variances = np.linalg.diag(ExpCovariance)
        return np.all(eigenvalueList >= 0)

    def checkType(self, var, dataType):
        """
            check parameter type
            Input Parameter:
                Npts, should be integer
        """
        if not isinstance(var, dataType):
            raise TypeError("Parameter must be {}".format(str(dataType)))
        return True

    def efficient_frontier(self, Npts=1000, delta=10, epsinon=1e-5, riskEpsinon=1e-5, isFilter=True):
        """
            求解有效前沿，通过异常捕获求解
            Input Parameter:
                Npts, default value 1000, int
        """
        self.checkType(Npts, int)
        try:
            return self.ComputeEF(Npts, delta, epsinon, riskEpsinon, isFilter)
        except Exception as diag:
            print("{}".format(diag))

    def constraint_frontier(self, factorMatrix, boundVector, Npts=1000, delta=10, epsinon=1e-5,
                            riskEpsinon=1e-5, isFilter=True):
        """
            带约束求解的异常捕获
            Input Parameters:
                factorMatrix, ndarray
                boundVector, ndarray
                Npts, default value 1000, int
        """
        self.checkType(Npts, int)
        risks = list()
        returns = list()
        portfolios = list()
        riskAversions = list()
        try:
            self.setInequalityBound(factorMatrix, boundVector)
            risks, returns, riskAversions, portfolios = self.efficient_frontier(Npts, delta, epsinon,
                                                                                riskEpsinon, isFilter)
        except ValueError as diag:
            print("Cause {0}, Please check the constraint".format(str(diag)))
        self.resetDefaultBound()
        return risks, returns, riskAversions, portfolios

    def compareFloat(self, var, flag=0.0, epsinon=1e-3):
        """
            浮点类型比较函数
            控制比较精度
        """
        self.checkType(var, float)
        self.checkType(flag, float)
        if math.fabs(var-flag) < epsinon:
        #var等于flag
            return 0
        elif var-flag > 0:
        #var大于flag
            return 1
        else:
        #var小于flag
            return -1

    def Solver(self, mu):
        """
            MVO单点求解器
            ms, risk aversion
        """
        # Convert to cvxopt matrices
        pbar = opt.matrix(self.ExpReturn.T)

        # Create constraint matrices
        A = opt.matrix(1.0, (1, self.n))
        b = opt.matrix(1.0)

        # Calculate efficient frontier weights using quadratic programming
        portfolio = solvers.qp(mu*self.S, -pbar, self.G, self.h, A, b)['x']
        # CALCULATE RISKS AND RETURNS FOR FRONTIER
        returns = blas.dot(pbar, portfolio)
        risks = np.sqrt(blas.dot(portfolio, self.S*portfolio))
        return risks, returns, portfolio

    def CheckEqual(self, dataList, epsinon=1e-5):
        """
            判断最后三个标准差是否相等
            dataList, 数据序列
            epsinon, 精度控制参数, 默认值1e-5
        """
        if not isinstance(dataList, type([])):
            raise TypeError("The Parameter should be type list")
        if len(dataList) <= 3:
            return False
        else:
            last3Risk = list(map(lambda x: x[1][0], dataList[-3:]))
            if self.compareFloat(last3Risk[0], last3Risk[1], epsinon) == 0 and\
               self.compareFloat(last3Risk[1], last3Risk[2], epsinon) == 0:
                return True
            else:
                return False

    def interpolation(self, maxRiskAversion, startPoint, Npts):
        """
            获取新内插点序列
        """
        # 最大风险厌恶系数反解最大X值
        maxValue = (math.log10(maxRiskAversion)+1.0)*Npts/5.0
        newXList = list(np.linspace(startPoint, maxValue, Npts))
        return [float(10**(5.0 * t/Npts - 1.0)) for t in newXList]

    def ComputeEF(self, Npts=1000, delta=10, epsinon=1e-5, riskEpsinon=1e-5, isFilter=True):
        """
            有效前沿计算主函数
            Npts,       points number on the efficient frontier
            delta,      searching step length
            epsinon,    searching tolerance
        """
        if self.checkType(epsinon, float):
            if operator.gt(epsinon, 0.1):
                raise ValueError("Epsinon should be less than 0.1")
        else:
            raise TypeError("Epsinon should be a float")
        # 初始化参数
        startPoint = 0.0
        endPoint = 10**(5.0 - 1.0)

        # 前向计算
        riskAversionPoint = startPoint
        tmpResultList = list()
        # 风险厌恶系数上限比较 不用控制精度
        while operator.lt(riskAversionPoint, endPoint):
            tmpResultList.append((riskAversionPoint, self.Solver(riskAversionPoint)))
            # 达到预设点数
            if len(tmpResultList) == Npts:
                print("Already Get Enough Points")
                break
            # 检查倒数三个elem的波动差异是否在精度内满足相等
            if self.CheckEqual(tmpResultList, epsinon):
                break
            riskAversionPoint += delta

        # 达到预设点数量，直接返回。否则，重新生成Npts个点计算
        if len(tmpResultList) == Npts:
            print("Directly Getting Result")
            if isFilter is True:
                return self.settleResult(self.filterResult(tmpResultList, riskEpsinon), isFilter)
            else:
                return self.settleResult(tmpResultList)
        else:
            print("Having Searched Risk Aversion Number: {}".format(len(tmpResultList)))
            maxRiskAversion = max(map(lambda x: x[0], tmpResultList[:-2]))
            print("Max Risk Aversion Coefficient: {}".format(maxRiskAversion))
            newRiskAversion = self.interpolation(maxRiskAversion, startPoint, Npts)
            print("New Risk Aversion Range: {} --> {}".format(min(newRiskAversion), max(newRiskAversion)))
            resultList = [(raPoint, self.Solver(raPoint)) for raPoint in newRiskAversion]
            if isFilter is True:
                return self.settleResult(self.filterResult(resultList, riskEpsinon), isFilter)
            else:
                return self.settleResult(resultList)

    def settleResult(self, resultList, isFilter=False):
        """
            返回结果整理函数
        """
        if isFilter is True:
            riskAversionList = list(map(lambda x: x[0], resultList))
            risksList = list(map(lambda x: x[1], resultList))
            returnsList = list(map(lambda x: x[2], resultList))
            portfolios = list(map(lambda x: x[3], resultList))
        else:
            sortedResult = sorted(resultList, key=operator.itemgetter(0), reverse=True)
            riskAversionList = list(map(lambda x: x[0], sortedResult))
            risksList = list(map(lambda x: x[1][0], sortedResult))
            returnsList = list(map(lambda x: x[1][1], sortedResult))
            portfolios = list(map(lambda x: x[1][2], sortedResult))
        return risksList, returnsList, riskAversionList, portfolios

    def filterResult(self, resultList, riskEpsinon=1e-5):
        """
            根据精度及对Risk升序排列
            resultList, (riskAversion, (risks, returns, portfolio))
            riskEpsinon, 结果筛选控制精度, 默认值1e-5
        """
        print(">>>Filtering And Sorting The Result")
        print(">>>Primeval Result Number is {}".format(len(resultList)))
        preElem = resultList[0]
        tmpResult = [(preElem[0], preElem[1][0], preElem[1][1], preElem[1][2])]
        for elem in resultList[1:]:
            if self.compareFloat(elem[1][0], preElem[1][0], riskEpsinon) != 0:
                tmpResult.append((elem[0], elem[1][0], elem[1][1], elem[1][2]))
            preElem = elem
        print(">>>Filtered {} Valid Result".format(len(tmpResult)))
        sortedResult = sorted(tmpResult, key=operator.itemgetter(1))
        print(">>>Filtered Max Risk Aversion: {}".format(max(map(lambda x: x[0], sortedResult))))
        return sortedResult
