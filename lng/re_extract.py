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

        m = re.search(PATTERN, line)
        if m:
            value1, value2 = m.group(1, 2)
            print 'Value %s, Value %s' % (value1, value2)
            print m.expand(r'Value: \1 Value: \2')
        else:
            print 'Not match'


if __name__ == '__main__':
    main()
