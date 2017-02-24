#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re


def repl_func(mo):
    s1 = mo.group(1)
    s2 = '*' * len(s1)
    return s2


def main():
    pattern = r'(\d+)'
    in_str = 'there are 203 birds sitting in 2 trees'
    out_str, count = re.subn(pattern, repl_func, in_str)
    print 'IN: %s' % in_str
    print 'Out: %s, Count: %d' % (out_str, count)


if __name__ == '__main__':
    main()
