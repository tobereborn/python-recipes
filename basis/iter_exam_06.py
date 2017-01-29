#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

mylist = xrange(1000)


def f(x):
    return x * 3


generator = (f(x) for x in mylist)


def main():
    for x in generator:
        print x


if __name__ == '__main__':
    main()
