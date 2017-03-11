#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame


def main():
    upBound = 0.9
    lowBound = 0.1
    fundList = ['HS.01', 'HS.02', 'HS.03']
    fundCnt = len(fundList)
    upFactorMatrix = np.eye(fundCnt)
    print('upFactorMatrix:')
    print(upFactorMatrix)
    lowFactorMatrix = np.eye(fundCnt) * -1.0
    print('lowFactorMatrix:')
    print(lowFactorMatrix)
    factorMatrix = np.vstack((upFactorMatrix, lowFactorMatrix))
    print('factorMatrix:')
    print(repr(factorMatrix))
    boundUp = np.ones((fundCnt, 1)) * min(upBound, 1.0)
    print('boundUp:')
    print(boundUp)
    boundLow = np.ones((fundCnt, 1)) * max(lowBound, 0.0) * -1.0
    print('boundLow:')
    print(boundLow)
    bound = np.vstack((boundUp, boundLow))
    print('bound:')
    print(bound)

    factorArray = np.zeros((2, len(fundList)))
    print('factorArray:')
    print(factorArray)
    boundArray = np.vstack((np.ones((1, 1)), np.zeros((1, 1))))
    print('boundArray:')
    print(boundArray)

    efPoints = DataFrame({'Risks': '1', 'Returns': '2', 'RiskAversions': '3'},
                         index=['Risks', 'Returns', 'RiskAversions'])
    print(efPoints)

    df = DataFrame([1, 2, 3, 4, 5])
    print(df)
    print(repr(df.mean().apply(lambda x: (1 + x) ** 2 - 1)))
    print(repr(df.cov() * 3))
    weq = DataFrame(np.array([.193400, .261300, .120900, .120900, .013400, .013400, .241800, .034900]))
    print(weq)
    print(weq.apply(lambda x: [elem / sum(x) for elem in x], axis=1))
    print(weq[0:8].values[-1])


if __name__ == '__main__':
    main()
