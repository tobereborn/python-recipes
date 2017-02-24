#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pandas as pd
import numpy as np


def main():
    # --------------- basics ---------------------- #
    dates = pd.date_range('1/1/2000', periods=8)
    print(repr(dates))
    df = pd.DataFrame(np.random.randn(8, 4), index=dates, columns=['A', 'B', 'C', 'D'])
    print(repr(df))
    panel = pd.Panel({'one': df, 'two': df - df.mean()})
    print(repr(panel))
    s = df['A']
    print(repr(s))
    print(repr(s[dates[5]]))
    print(repr(panel['two']))
    print(repr(panel[['two', 'one']]))
    # in place transform
    print(df)
    df[['A', 'B']] = df[['B', 'A']]
    print(df)

    # ------------ attribute access --------------#
    sa = pd.Series([1, 2, 3], index=list('abc'))
    dfa = df.copy()
    print(sa.b)
    print(dfa.A)
    print(panel.one)
    sa.a = 5
    print(sa)
    dfa.A = list(range(len(dfa.index)))
    print(dfa)
    x = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    print(x)

    # assign a dict
    x.iloc[1] = dict(x=9, y=9)
    print(x)

    # ---------slicing ranges ---------#
    s = pd.Series([1, 2, 3, 4, 5, 6], index=list('abcdef'))
    print(s[:5])
    print(repr(s[::2]))
    print(s[::-1])
    s2 = s.copy()
    print(s2[:5])
    # data frame slicing row
    print(df[:3])
    print(df[::-1])

    # ----------- select by label --------------- #
    dfl = pd.DataFrame(np.random.randn(5, 4), columns=list('ABCD'), index=pd.date_range('20130101', periods=5))
    print(dfl)
    # wrong index
    # print(dfl.loc[2:3])
    print(dfl.loc['20130102':'20130104'])
    s1 = pd.Series(np.random.randn(6), index=list('abcdef'))
    print(s1)
    print(s1.loc['c':])
    print(s1.loc['b'])
    s1.loc['c':] = 0
    print(s1)
    dfl = pd.DataFrame(np.random.rand(6, 4), index=list('abcdef'), columns=list('ABCD'))
    print(dfl)
    print(dfl.loc[['a', 'b', 'd'], :])
    print(dfl.loc['d':, 'A':'C'])
    # getting a cross section
    print(dfl.loc['a'])
    print(dfl.xs('a'))
    # boolean array
    print(dfl.loc['a'] > 0)
    print(dfl.loc[:, dfl.loc['a'] > 0.5])
    # get value explicitly
    print(dfl.loc['a', 'A'])
    print(dfl.get_value('a', 'A'))


if __name__ == '__main__':
    main()
