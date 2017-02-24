#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(s)
    dates = pd.date_range('20130101', periods=6)
    print(dates)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print(df)
    data = np.zeros((2,), dtype=[('A', 'i4'), ('B', 'f4'), ('C', 'a10')])
    print(data)


if __name__ == '__main__':
    main()
