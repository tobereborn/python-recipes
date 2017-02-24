#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


class Kls(object):
    no_inst = 0

    def __init__(self, data):
        self.data = data
        Kls.no_inst += 1

    def printd(self):
        print self.data

    @classmethod
    def get_no_of_inst(cls):
        return cls.no_inst


def main():
    kls1 = Kls('123')
    kls1.printd()
    print kls1.get_no_of_inst()
    print Kls.get_no_of_inst()
    kls2 = Kls('456')
    kls2.printd()
    print kls2.get_no_of_inst()
    print Kls.get_no_of_inst()


if __name__ == '__main__':
    main()
