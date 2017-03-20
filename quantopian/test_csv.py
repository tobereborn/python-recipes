#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-23

from zipline.api import order_target_percent, get_datetime, sid


def initialize(context):
    pass


def handle_data(context, data):
    print('data: ', data.current([sid(0), sid(1)], ['volume', 'price']))
    iNumEqt = len(data)
    print "get_datetime", get_datetime(), "iNumEqt=", iNumEqt
    fW = 1.0 / iNumEqt
    for S in data:
        print "Ordering", fW, " of ", S.symbol
        order_target_percent(S, fW)
