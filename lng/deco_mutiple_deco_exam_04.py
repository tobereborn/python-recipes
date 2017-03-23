#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-7


def b(fn):
    return lambda s: r'<b>%s<\b>' % fn(s)


def em(fn):
    return lambda s: r'<em>%s<\em>' % fn(s)


@b
@em
def greet(name):
    return 'Hello %s' % name


def sayhi(name):
    return 'Hi %s' % name


sayhi = em(sayhi)
sayhi = b(sayhi)


def main():
    print(greet('jack'))
    print(sayhi('tom'))


if __name__ == '__main__':
    main()
