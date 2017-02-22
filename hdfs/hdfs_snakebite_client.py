#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-22


from snakebite.client import Client
import pandas as pd


def as_dataframe(rows):
    columns = ['id', 'name']
    df = pd.DataFrame.from_records(rows, columns)
    return df


def main():
    client = Client('localhost', 9000)
    # for f in client.ls(['/user/hive'], True):
    #     print(f)
    df = pd.DataFrame()
    rows = client.text(['/user/hive/warehouse/test.db/employee/ds=20170221/employee.tsv'])


if __name__ == '__main__':
    main()
