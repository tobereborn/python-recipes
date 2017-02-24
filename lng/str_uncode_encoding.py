#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-16


def main():
    s = u'中文jack-{0}'.format(1)
    print(s)
    print(type(s))
    print(s.encode('utf-8'))

if __name__ == '__main__':
    main()
