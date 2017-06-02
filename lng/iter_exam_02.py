#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

DATA = ['lemon',
        'lime',
        'grape',
        'apple',
        'pear',
        'watermelon',
        'canteloupe',
        'honeydew',
        'orange',
        'grapefruit']


def make_producer(collection, excludes):
    gen = (item for item in collection if item not in excludes)
    return gen


def main():
    iter1 = make_producer(DATA, ('apple', 'orange', 'honeydew'))
    print('%s' % iter1)
    for fruit in iter1:
        print(fruit)


if __name__ == '__main__':
    main()
