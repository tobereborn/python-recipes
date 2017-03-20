#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def main():
    dtypes = ['int64', 'float64', 'datetime64[ns]', 'timedelta64[ns]', 'complex128', 'object', 'bool']
    n = 5000
    data = dict([(t, np.random.randint(100, size=n).astype(t)) for t in dtypes])

    dt=pd.DataFrame(data)
    print(dt)


if __name__ == '__main__':
    main()
