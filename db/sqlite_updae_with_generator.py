#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

import sqlite3
import string


def users():
    for c in string.lowercase:
        yield ord(c), c


def main():
    conn = None
    try:
        conn = sqlite3.connect('test.db')
        print(conn.isolation_level)
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('create table if not exists user(id int primary key, name varchar(20))')
            cursor.execute('delete from user')
            cursor.executemany('insert into user (id ,name) values (?,?)', users())
            print('insert counts: %s' % cursor.rowcount)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print('Error when executing sql and rollbacked, args: %s, message: %s' % (e.args, e.message))
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
