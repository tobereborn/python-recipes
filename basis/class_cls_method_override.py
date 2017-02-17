#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


class Base(object):
    def __init__(self, size):
        self.size = size

    def add(self, num):
        print('Base.add(num)')
        self.size += num

    def printd(self):
        print('size=%s' % self.size)


class SubA(Base):
    def __init__(self, size):
        super(SubA, self).__init__(size)

    def add(self, num):
        print('SubA.add(num)')
        self.size += 2 * num


def main():
    base = Base(1)
    base.printd()
    a = SubA(2)
    a.add(2)
    a.printd()
    base = a
    base.printd()


if __name__ == '__main__':
    main()
