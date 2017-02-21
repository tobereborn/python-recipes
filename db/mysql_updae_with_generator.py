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
    'charset': 'utf8',
}


def users(size=100):
    for i in xrange(1, size):
        yield (i, u'中文jack-{0}'.format(i).encode('utf8'))


# Is is not working, only list or tuple is accepted
def main():
    conn = None
    try:
        conn = MySQLdb.connect(**CONFIG)
        # print(conn.isolation_level)
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('create table if not exists user(id int primary key, name varchar(20))')
            cursor.execute('delete from user')
            cursor.executemany('insert into user (id ,name) values (%s,%s)', users())
            print('insert counts: %s' % cursor.rowcount)
            conn.commit()
        except MySQLdb.Error as e:
            conn.rollback()
            print('Error when executing sql and rollbacked, args: %s, message: %s' % (e.args, e.message))
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
