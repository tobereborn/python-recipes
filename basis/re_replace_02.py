#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re

PATTERN = re.compile('aa([0-9]*)bb([0-9]*)cc')


def main():
    while 1:
        line = raw_input('Enter a line ("q" to quit):')
        if line == 'q':
            break
        mo = PATTERN.search(line)
        if mo:
            value1, value2 = mo.group(1, 2)
            start1 = mo.start(1)
            end1 = mo.end(1)
            start2 = mo.start(2)
            end2 = mo.end(2)
            print 'value1: %s start1: %d end1: %d' % (value1, start1, end1)
            print 'value2: %s start2: %d end2: %d' % (value2, start2, end2)
            repl1 = raw_input('Enter replacement #1:')
            repl2 = raw_input('Enter replacement #2:')
            newline = (line[:start1] + repl1 + line[end1:start2] + repl2 + line[end2:])
            print 'newline: %s' % newline
        else:
            print 'no match'


if __name__ == '__main__':
    main()
