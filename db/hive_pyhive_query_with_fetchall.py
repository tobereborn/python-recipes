#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

from pyhive import hive
from TCLIService.ttypes import TOperationState
from db import cusor_2_dataframe as c2d

CONFIG = {
    'host': 'localhost', 'port': 10000, 'username': 'weizhenjin', 'database': 'test', 'auth': 'NONE'
}


# Is is not working, only list or tuple is accepted
def main():
    cursor = hive.connect(**CONFIG).cursor()
    cursor.execute('SELECT * FROM employee limit 10 ', async=True)

    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
        logs = cursor.fetch_logs()
        for message in logs:
            print(message)

        # If needed, an asynchronous query can be cancelled at any time with:
        # cursor.cancel()

        status = cursor.poll().operationState
    print(cursor.description)
    print(c2d.as_pandas(cursor))


if __name__ == '__main__':
    main()
