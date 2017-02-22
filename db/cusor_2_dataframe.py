#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-22


def as_pandas(cursor):
    """Return a pandas `DataFrame` out of an impyla cursor.
    This will pull the entire result set into memory.  For richer pandas-like
    functionality on distributed data sets, see the Ibis project.
    Parameters
    ----------
    cursor : The cursor object that has a result set waiting to be fetched.
    Returns
    -------
    DataFrame
    """
    from pandas import DataFrame
    for metadata in cursor.description:
        print(metadata)
    names = [metadata[0] for metadata in cursor.description]
    return DataFrame.from_records(cursor.fetchall(), columns=names)


def main():
    pass


if __name__ == '__main__':
    main()
