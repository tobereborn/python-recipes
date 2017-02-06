#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6

IND = 'ON'


def checkind():
    return IND == 'ON'


class Kls(object):
    def __init__(self, data):
        self.data = data

    def printd(self):
        print self.data

    def do_reset(self):
        if checkind():
            print 'Reset done fro {0}'.format(self.data)

    def set_db(self):
        if checkind():
            print 'Set db for {0}'.format(self.data)


def main():
    kls1 = Kls('a')
    kls1.printd()
    kls1.do_reset()
    kls1.set_db()


if __name__ == '__main__':
    main()
