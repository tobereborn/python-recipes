#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-23


import time
from datetime import datetime, timedelta

import dateutil


def to_timestamp(dt_str, tz_str):
    dtz_str = dt_str + ' ' + tz_str.replace(':', '')
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    # dt = datetime.strptime(dtz_str, '%Y-%m-%d %H:%M:%S %Z%z')
    return dt.replace(tzinfo=timezone(timedelta(hours=7)))


def main():
    now = datetime.now()
    print('now: %s' % now)
    print(now.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    ts = time.mktime(now.timetuple())
    print('ts: %s' % ts)
    ts_2_dt = datetime.fromtimestamp(ts)
    print('ts_2_dt: %s' % ts_2_dt)
    dt = datetime(2017, 2, 22, 10, 20, 22)
    # print(dt)
    dt1 = datetime.strptime('2015-6-1 08:10:30', '%Y-%m-%d %H:%M:%S')
    print(dt1.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    print(to_timestamp('2015-6-1 08:10:30', 'UTC+7:00'))


if __name__ == '__main__':
    main()
