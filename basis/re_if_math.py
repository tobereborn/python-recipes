#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re


def main():
    pat = re.compile('aa[bc]*dd')

    while 1:
        line = raw_input('Enter a line ("q" to quit):')
        if line == 'q':
            break
        if pat.search(line):
            print 'Matched:', line
        else:
            print "No match:", line


if __name__ == '__main__':
    main()
