#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

import sqlite3


def main():
    conn = None
    try:
        conn = sqlite3.connect('test.db')
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('select * from user where id >=? and id <=?', ('1', '50'))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print('Error when executing sql, args: %s, message: %s' % (e.args, e.message))
        finally:
            if cursor:
                cursor.close()
    except sqlite3.Error as e:
        print('Error when connecting to db, args: %s, message: %s' % (e.args, e.message))
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
