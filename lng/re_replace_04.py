#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re, string

PATTERN = re.compile('[a-z]+')


def replacer(mo):
    return string.upper(mo.group(0))


def main():
    print 'Upper'
    while 1:
        line = raw_input('Enter a line ("q" to quit):')
        if line == 'q':
            break
        result1 = PATTERN.sub(replacer, line)
        result2=PATTERN.sub(lambda mo:string.upper(mo.group(0)),line)
        print 'Result1: %s, result2: %s' % (result1,result2)


if __name__ == '__main__':
    main()
