#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-23

from zipline.api import order_target_percent, get_datetime


def initialize(context):
    pass


def handle_data(context, data):
    iNumEqt = len(data)
    print "get_datetime", get_datetime(), "iNumEqt=", iNumEqt
    fW = 1.0 / iNumEqt
    for S in data:
        print "Ordering", fW, " of ", S.symbol
        order_target_percent(S, fW)
