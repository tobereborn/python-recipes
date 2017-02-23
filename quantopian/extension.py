#!/usr/bin/env python
# -*- coding: utf-8 -*-


from zipline.data.bundles import register
from zipline.data.bundles.viacsv import viacsv

eqSym = {
    "N225",
}

register(
    'csv',  # name this whatever you like
    viacsv(eqSym),
)
