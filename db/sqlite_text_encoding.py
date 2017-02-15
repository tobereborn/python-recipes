#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

import sqlite3

# unicode
AUSTRIA = u"\xd6sterreich"


def main():
    conn = None
    try:
        conn = sqlite3.connect('test.db')
        print(conn.isolation_level)
        cursor = None
        try:
            cursor = conn.cursor()

            # by default, rows are returned as Unicode
            cursor.execute('select ?', (AUSTRIA,))
            row = cursor.fetchone()
            assert type(row[0]) is unicode

            # but we can make sqlite3 always return bytestrings ...
            conn.text_factory = str
            cursor.execute('select ?', (AUSTRIA,))
            row = cursor.fetchone()
            assert type(row[0]) is str
            # the bytestrings will be encoded in UTF-8, unless you stored garbage in the database...
            assert row[0] == AUSTRIA.encode('utf-8')

            # we can also implement a custom text_factory ...
            # here we implement one that will ignore Unicode characters that cannot be
            # decoded from UTF-8
            conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
            cursor.execute('select ?', ("this is latin1 and would normally create errors" +
                                        u"\xe4\xf6\xfc".encode("latin1"),))
            row = cursor.fetchone()
            print(row)
            assert type(row[0]) is unicode

            # sqlite3 offers a built-in optimized text_factory that will return bytestring
            # objects, if the data is in ASCII only, and otherwise return unicode objects
            conn.text_factory = sqlite3.OptimizedUnicode
            cursor.execute('select ?', (AUSTRIA,))
            row = cursor.fetchone()
            assert type(row[0]) is unicode

            cursor.execute("select ?", ("Germany",))
            row = cursor.fetchone()
            assert type(row[0]) is str

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
