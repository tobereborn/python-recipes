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

    # ----------- select by position --------------- #
    s1 = pd.Series(np.random.rand(5), index=list(range(0, 10, 2)))
    print(s1)
    print(s1.iloc[:3])
    print(s1.iloc[3])
    s1.iloc[:3] = 0
    print(s1)
    dfl = pd.DataFrame(np.random.randn(6, 4), index=list(range(0, 12, 2)), columns=list(range(0, 8, 2)))
    print(dfl)
    print(dfl.iloc[:3])
    print(dfl.iloc[1:5, 2:4])
    # select via integer list
    print(dfl.iloc[[1, 3, 5], [1, 3]])
    print(dfl.iloc[1:3, :])
    print(dfl.iloc[:, 1:3])
    print(dfl.iloc[1, 1])
    print(dfl.iat[1, 1])
    print(dfl.iloc[1])
    # print(dfl.xs(1))

    # out of range slie indexes are handled gracefully
    x = list('abcdef')
    print(x)
    print(x[4:10])
    print(x[8:10])
    s = pd.Series(x)
    print(s)
    print(s.iloc[4:10])
    print(s.iloc[8:10])

    dfl = pd.DataFrame(np.random.randn(5, 2), columns=list('AB'))
    print(dfl)
    print(dfl.iloc[:, 2:3])
    print(dfl.iloc[:, 1:3])
    print(dfl.iloc[4:6])

    # a single indexer that is out of bounds will raise error
    # print(dfl.iloc[:, 4])
    # a list of indexers where any elements is out of bounds will raise error
    # print(dfl.iloc[[4, 5, 6]])

    # --------------- selecting random samples ------------#
    s = pd.Series([0, 1, 2, 3, 4, 5])
    # return 1 sample
    print(s.sample())
    print(s.sample(n=3))
    print(s.sample(frac=0.5))
    # without replacement
    print(s.sample(n=6, replace=False))
    # with replacement
    print(s.sample(n=6, replace=True))
    example_weights = [0, 0, 0.2, 0.2, 0.2, 0.4]
    print(s.sample(n=3, weights=example_weights))
    # weights will be re-normalized automatically
    example_weights2 = [0.5, 0, 0, 0, 0, 0]
    print(s.sample(n=1, weights=example_weights2))

    df2 = pd.DataFrame({'col1': [9, 8, 7, 6], 'weight_column': [0.5, 0.4, 0.1, 0]})
    print(df2.sample(n=3, weights='weight_column'))
    df3 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [2, 3, 4]})
    print(df3)
    # sample columns with axis argument
    print(df3.sample(n=1, axis=1))

    df4 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [2, 3, 4]})
    # with a given seed, the sample will always drwa the same rows
    print(df4.sample(n=2, random_state=2))
    print(df4.sample(n=2, random_state=2))

    # --------------------- setting with enlargement ----------------#
    se = pd.Series([1, 2, 3])
    print(se)
    # append
    se[5] = 5
    print(se)

    dfi = pd.DataFrame(np.arange(6).reshape(3, 2), columns=['A', 'B'])
    print(dfi)
    dfi.loc[:, 'C'] = dfi.loc[:, 'A']
    print(dfi)
    dfi.loc[3] = 5
    print(dfi)

    # --------------- fast scalar value getting and setting -------------------#
    print(dfi.at[3, 'A'])

    # --------------- boolean indexing ------------------------#
    # | = or, & = and , ~ = not
    s = pd.Series(range(-3, 4))
    print(s)
    print(s[s > 0])
    print(s[(s < -1) | (s > 0.5)])
    print(s[~(s < 0)])
    print(dfi[dfi['A'] > 0])

    df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'three', 'two', 'one', 'six'],
                        'b': ['x', 'y', 'y', 'x', 'y', 'x', 'x'],
                        'c': np.random.randn(7)
                        })
    print(df2)
    criterion = df2['a'].map(lambda x: x.startswith('t'))
    print(df2[criterion])
    print(df2[[x.startswith('t') for x in df2['a']]])
    print(df2[criterion & (df2['b'] == 'x')])
    print(df2.loc[criterion & (df2['b'] == 'x'), 'b':'c'])

    # --------------------- indexing with isin -------------- #
    s = pd.Series(np.arange(5), index=np.arange(5)[::-1], dtype='int64')
    print(s)
    print(s.isin([2, 4, 6]))
    print(s[s.isin([2, 4, 6])])
    # apply to index as well
    print(s[s.index.isin([2, 4, 6])])
    # compar it to the following
    print(s[[2, 4, 6]])

    # multiIndex
    s_mi = pd.Series(np.arange(6), index=pd.MultiIndex.from_product([[0, 1], ['a', 'b', 'c']]))
    print(s_mi)
    print(s_mi.iloc[s_mi.index.isin([(1, 'a'), (2, 'b'), (0, 'c')])])
    print(s_mi.iloc[s_mi.index.isin(['a', 'c', 'e'], level=1)])

    df = pd.DataFrame({'vals': [1, 2, 3, 4],
                       'ids': ['a', 'b', 'f', 'n'],
                       'ids2': ['a', 'n', 'c', 'n']})
    print(df)
    values = ['a', 'b', 1, 3]
    print(df.isin(values))
    values = {'ids': ['a', 'b'], 'vals': [1, 3]}
    print(df.isin(values))
    values = {'ids': ['a', 'b'], 'ids2': ['a', 'c'], 'vals': [1, 3]}
    row_mask = df.isin(values).all(1)
    print(df[row_mask])

    # -------------------- the where() method and masking ----------------------#
    # return the same shape as the original data
    s = pd.Series(np.arange(5), index=np.arange(5)[::-1], dtype='int64')
    print(s)
    print(s.where(s > 0))
    df = pd.DataFrame(np.random.randn(8, 4), columns=list('ABCD'), index=pd.date_range('20000101', periods=8))
    print(df)
    print(df[df < 0])
    # other -df argument to replace values where the condition is false
    print(df.where(df < 0, -df))

    s2 = s.copy()
    s2[s2 < 0] = 0
    print(s2)
    df2 = df.copy()
    df2[df2 < 0] = 0
    print(df2)
    df_org = df.copy()
    df_org.where(df > 0, -df, inplace=True)
    print(df_org)

    # alignment
    df2 = df.copy()
    print(df2[1:4])
    print(df2[df2[1:4] > 0])
    df2[df2[1:4] > 0] = 3
    print(df2)
    df2 = df.copy()
    df2w = df2.where(df2 > 0, df2['A'], axis='index')
    print(df2w)

    # mask is the inverse of where
    print(s.mask(s >= 0))
    print(df.mask(df >= 0))

    # ------------------ duplicate data ---------------------#
    df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'two', 'two', 'three', 'four'],
                        'b': ['x', 'y', 'x', 'y', 'x', 'x', 'x'],
                        'c': np.random.randn(7)})
    print(df2)
    print(df2.duplicated('a'))
    print(df2.duplicated('a', keep='last'))
    print(df2.duplicated('a', keep=False))
    print(df2.drop_duplicates('a'))
    print(df2.drop_duplicates('a', keep='last'))
    print(df2.drop_duplicates('a', keep=False))
    print(df2.duplicated(['a', 'b']))
    print(df2.drop_duplicates(['a', 'b']))
    df3 = pd.DataFrame({'a': np.arange(6),
                        'b': np.random.randn(6)}, index=['a', 'a', 'b', 'c', 'b', 'a'])
    print(df3)
    print(df3.index.duplicated())

    # ------------- dict-like get() method -----------------#
    s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
    print(s.get('a'))
    print(s.get('x', default=-1))

    # -------------- select() method -----------------------#
    print(df)
    print(df.select(lambda x: x == 'A', axis=1))

    # --------------- lookup() method -----------------------#
    dflookup = pd.DataFrame(np.random.rand(20, 4), columns=list('ABCD'))
    print(dflookup)
    print(dflookup.lookup(list(range(0, 10, 2)), ['B', 'C', 'A', 'B', 'D']))

    # ------------------- index object -----------------------#
    index = pd.Index(list(range(5)), name='rows')
    print(index)
    columns = pd.Index(['A', 'B', 'C'], name='cols')
    print(columns)
    df = pd.DataFrame(np.random.randn(5, 3), index=index, columns=columns)
    print(df)
    print(df['A'])

    # setting metadata
    ind = pd.Index([1, 2, 3])
    print(ind)
    print(ind.rename('apple'))
    ind.set_names(["apple2"], inplace=True)
    print(ind)
    ind.name = 'bob'
    print(ind)
    index = pd.MultiIndex.from_product([range(3), ['one', 'two'], ['c', 'd']], names=['first', 'second', 'three'])
    print(index)
    print(index.levels[1])
    print(index.set_levels(['a', 'b'], level=1))
    print(index)

    # Set operations on Index objects
    a = pd.Index(['c', 'b', 'a'])
    b = pd.Index(['c', 'e', 'd'])
    print(a | b)
    print(a & b)
    print(a.difference(b))
    print(b.difference(a))
    idx1 = pd.Index([1, 2, 3, 4])
    idx2 = pd.Index([2, 3, 4, 5])
    print(idx1.sym_diff(idx2))
    print(idx1 ^ idx2)
    # fill missing
    idx1 = pd.Index([1, np.nan, 3, 4])
    print(idx1)
    print(idx1.fillna(2))
    idx2 = pd.DatetimeIndex([pd.Timestamp('2011-01-01'), pd.NaT, pd.Timestamp('2011-01-03')])
    print(idx2)
    print(idx2.fillna(pd.Timestamp('2011-01-02')))

    # --------- set /reset index------------------------------#
    print(df)


if __name__ == '__main__':
    main()
