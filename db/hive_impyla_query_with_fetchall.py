#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-15

"""
So I found the problem with PLAIN sasl. It was because the username and password must be set and non-empty or the
connection fails, even though they are not really used. When you enable LDAP it will force impyla to use PLAIN SASL,
but will doesn't actually use LDAP anywhere for authentication.This allows the connection to succeed against Hive.

For example, this now works to connect to Hive using the PLAIN SASL:
conn = connect(host='vd0214.halxg.cloudera.com', port=10000, use_ldap=True, ldap_user='user', ldap_password='pass')

"""

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
