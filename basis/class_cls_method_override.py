#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


class Base(object):
    def __init__(self, size):
        self.size = size

    def add(self, num):
        print('Base.add(num)')
        self.size += num

    def print(self):
        print('size=%s' % self.size)


class SubA(Base):
    def __init__(self, size):
        super().__init__(size)

    def add(self, num):
        print('SubA.add(num)')
        self.size += 2 * num


def main():
    base = Base(1)
    base.print()
    a = SubA(2)
    a.add(2)
    a.print()
    base = a
    base.print()


if __name__ == '__main__':
    main()
