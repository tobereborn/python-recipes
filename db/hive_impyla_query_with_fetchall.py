#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

# import mysql.connector
from impala.dbapi import connect

CONFIG = {
    'host': 'localhost',
    'user': 'weizhenjin',
    'password': 'weizhenjin',
    'database': 'test',
    'port': 10000,
    'auth_mechanism': 'PLAIN',
}


# Is is not working, only list or tuple is accepted
def main():
    conn = connect(**CONFIG)
    cur = conn.cursor()
    cur.execute('select * from employee')
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == '__main__':
    main()
