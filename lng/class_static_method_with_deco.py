#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6

IND = 'ON'


class Kls(object):
    def __init__(self, data):
        self.data = data

    def printd(self):
        print self.data

    @staticmethod
    def checkind():
        return IND == 'ON'

    def do_reset(self):
        if self.checkind():
            print 'Reset done fro {0}'.format(self.data)

    def set_db(self):
        if self.checkind():
            print 'Set db for {0}'.format(self.data)


def main():
    kls1 = Kls('b')
    kls1.printd()
    kls1.do_reset()
    kls1.set_db()


if __name__ == '__main__':
    main()
