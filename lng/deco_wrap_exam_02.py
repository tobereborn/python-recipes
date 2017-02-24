#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


def decorator(fn):
    def inner(n):
        return fn(n) + 1

    return inner


# using decorator
@decorator
def f(n):
    return 2*n


# using function
def g(n):
    return 2*n


g = decorator(g)


def main():
    print f(1)
    print g(1)


if __name__ == '__main__':
    main()
