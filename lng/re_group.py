#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re

Targets = ['There are <<25>> sparrows.',
           'I see <<15>> finches.',
           'There is nothing here.', ]


def main():
    pattern = re.compile('<<([0-9]*)>>')
    for line in Targets:
        m = pattern.search(line)
        if m:
            # print m.groups()
            print 'Value: %s' % m.group(1)
        else:
            print 'No match'


if __name__ == '__main__':
    main()
