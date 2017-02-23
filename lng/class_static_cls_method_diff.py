#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


class Kls(object):
    def __init__(self, data):
        self.data = data

    def printd(self):
        print self.data

    @classmethod
    def classmethod(*arg):
        print 'Class Method:', arg

    @staticmethod
    def staticmethod(*arg):
        print 'Static Method:', arg


def main():
    kls = Kls('Kls')
    kls.printd()
    # Kls.printd()
    kls.classmethod()
    Kls.classmethod()
    kls.staticmethod()
    Kls.staticmethod()


if __name__ == '__main__':
    main()
