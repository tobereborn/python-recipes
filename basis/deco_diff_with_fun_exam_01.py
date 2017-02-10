#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


def wrap_with_prints(fn):
    print 'wrap_with_prints runs only once'

    def wrapped():
        print 'about to run %s' % fn.__name__
        fn()
        print 'done running %s' % fn.__name__

    return wrapped


@wrap_with_prints
def func_to_decorate():
    print 'running func_to_decorate'


def main():
    func_to_decorate()
    func_to_decorate()
    func_to_decorate()


if __name__ == '__main__':
    main()
