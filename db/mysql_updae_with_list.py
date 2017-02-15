#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

import mysql.connector

CONFIG = {
    'user': 'root',
    'password': 'mysql@1234',
    'host': 'localhost',
    'database': 'test_py',
    # 'raise_on_warnings': True,
}


def main():
    conn = None
    try:
        conn = mysql.connector.connect(**CONFIG)
        # print(conn.isolation_level)
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('create table if not exists user(id int primary key, name varchar(20))')
            cursor.execute('delete from user')
            users = []
            for i in xrange(1, 100):
                users.append((i, 'jack-{0}'.format(i)))
            cursor.executemany('insert into user (id ,name) values (%s,%s)', users)
            print('insert counts: %s' % cursor.rowcount)
            conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            print('Error when executing sql and rollbacked, args: %s, message: %s' % (e.args, e.message))
        finally:
            if cursor:
                cursor.close()
    except mysql.connector.Error as e:
        print('Error when connecting to db, args: %s, message: %s' % (e.args, e.message))
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
