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


class Users(object):
    def __init__(self, count):
        self.count = count
        self.id = 0

    def __iter__(self):
        return self

    def next(self):
        if self.id > self.count:
            raise StopIteration
        else:
            self.id += 1
            return self.id - 1, 'jack-{0}'.format(self.id - 1)


def test():
    for user in Users(100):
        print(user)


# Is is not working, only list or tuple is accepted
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
            cursor.executemany('insert into user (id ,name) values (?,?)', Users(100))
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
    test()
