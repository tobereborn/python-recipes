#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys, re


def main():
    mo = re.search(r'h:(\d*) w:(\d*)', 'h:123 w:456')
    result=mo.expand(r'Height: \1 Width: \2')
    print result


if __name__ == '__main__':
    main()
