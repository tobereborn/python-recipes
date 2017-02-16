#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

# import mysql.connector
import MySQLdb

CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'mysql@1234',
    'db': 'test_py',
    'port': 3306,
    'charset':'utf8'
}

# Is is not working, only list or tuple is accepted
def main():
    conn = None
    try:
        conn = MySQLdb.connect(**CONFIG)
        # print(conn.isolation_level)
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('select * from user where id>=%s and id <=%s', (0, 100))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except MySQLdb.Error as e:
            print('Error when executing query, args: %s, message: %s' % (e.args, e.message))
        finally:
            if cursor:
                cursor.close()
    except MySQLdb.Error as e:
        print('Error when connecting to db, args: %s, message: %s' % (e.args, e.message))
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
