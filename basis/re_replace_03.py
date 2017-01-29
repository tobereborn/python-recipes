#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re

PATTERN = re.compile('[0-9]+')


def main():
    print 'Replacing decimal digits'
    while 1:
        line = raw_input('Enter a line ("q" to quit):')
        if line == 'q':
            break
        replacement = raw_input('Enter a remplement:')
        result = PATTERN.sub(replacement,line)
        print 'Result: %s' % result


if __name__ == '__main__':
    main()
