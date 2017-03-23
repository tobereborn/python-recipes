#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

# import mysql.connector
import pyhs2

CONFIG = {
    'host': 'localhost',
    'user': 'weizhenjin',
    'password': 'weizhenjin',
    'database': 'test',
    'port': 10000,
    'authMechanism': 'PLAIN',
}


# Is is not working, only list or tuple is accepted
def main():
    try:
        with pyhs2.connect(**CONFIG) as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('select * from employee limit 1')
                    print(cur.getSchema())
                    rows = cur.fetchall()
                    for row in rows:
                        print(row[1].decode('utf-8'))
            except Exception as e:
                print('Executing sql error %s' % e)
    except Exception as e:
        print('Connection error: %s' % e)


if __name__ == '__main__':
    main()
