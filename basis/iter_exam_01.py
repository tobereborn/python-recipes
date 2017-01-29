#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

def generateItems(seq):
    for item in seq:
        yield 'item: %s' % item


def main():
    anIter = generateItems([])
    print 'dir(agIter):', dir(anIter)
    anIter = generateItems([111, 222, 333])
    for x in anIter:
        print x
    anIter = generateItems(['aaa', 'bbb', 'ccc'])
    print anIter.next()
    print anIter.next()
    print anIter.next()
    print anIter.next()


if __name__ == '__main__':
    main()
