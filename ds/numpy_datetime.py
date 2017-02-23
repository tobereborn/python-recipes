#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np


def main():
    # -------basic dattimes ---------#
    dt = np.datetime64('2005-02-05')
    print(repr(dt))
    dt = np.datetime64('2005-02')
    print(repr(dt))
    dt = np.datetime64('2005-01', 'D')
    print(repr(dt))
    dt = np.datetime64('2005-02-25T03:30')
    print(repr(dt))
    a = np.array(['2015-07-13', '2016-01-13', '2010-08-13'], dtype='datetime64')
    print(repr(a))
    a = np.array(['2001-01-01T12:00', '2002-02-03T13:56:03.172'], dtype='datetime64')
    print(repr(a))
    a = np.arange('2005-02', '2005-03', dtype='datetime64[D]')
    print(repr(a))
    print(np.datetime64('2005') == np.datetime64('2005-01-01'))
    print(np.datetime64('2005-01-01T15Z') == np.datetime64('2005-01-01T15:00:00Z'))

    # -------timedelta arithmetic ---------#
    delta = np.datetime64('2009-01-01') - np.datetime64('2008-01-01')
    print(repr(delta))
    delta = np.datetime64('2009') + np.timedelta64(20, 'D')
    print(repr(delta))
    delta = np.datetime64('2011-06-15T00:00') + np.timedelta64(12, 'h')
    print(repr(delta))
    delta = np.timedelta64(1, 'W') / np.timedelta64(1, 'D')
    print(repr(delta))
    a = np.timedelta64(1, 'Y')
    print(repr(a))
    delta = np.timedelta64(a, 'M')
    print(repr(delta))
    #  not working
    # delta = np.timedelta64(a, 'D')
    # print(repr(delta))

    # ------------business day functionality--------------- #
    dt = np.busday_offset('2011-06-23', 1)
    print(repr(dt))
    dt = np.busday_offset('2011-06-23', 2)
    print(repr(dt))

    # input day falls on the weekend, raise exception by default
    # dt = np.busday_offset('2011-06-25', 2)
    # print(repr(dt))

    dt = np.busday_offset('2011-06-25', 0, roll='forward')
    print(repr(dt))

    dt = np.busday_offset('2011-06-25', 2, roll='forward')
    print(dt)

    dt = np.busday_offset('2011-06-25', 0, roll='backward')
    print(dt)

    dt = np.busday_offset('2011-06-25', '2', roll='backward')
    print(dt)

    # the first business day on or after a date
    dt = np.busday_offset('2011-03-20', 0, roll='forward')
    print(repr(dt))
    dt = np.busday_offset('2011-03-22', 0, roll='forward')
    print(repr(dt))

    # the first business day strictly after a date
    dt = np.busday_offset('2011-03-20', 1, roll='backward')
    print(repr(dt))
    dt = np.busday_offset('2011-03-22', 1, roll='backward')
    print(repr(dt))

    # Computing Mother's day, which is on the second sunday in may
    dt = np.busday_offset('2012-05', 1, roll='forward', weekmask='Sun')
    print(dt)

    print(np.is_busday(np.datetime64('2011-07-15')))
    print(np.is_busday(np.datetime64('2011-07-16')))
    print(np.is_busday(np.datetime64('2011-07-16'), weekmask='Sat Sun'))
    a = np.arange(np.datetime64('2011-07-11'), np.datetime64('2011-07-18'))
    print(np.is_busday(a))

    count = np.busday_count(np.datetime64('2011-07-11'), np.datetime64('2011-07-18'))
    print(count)
    count = np.busday_count(np.datetime64('2011-07-18'), np.datetime64('2011-07-11'))
    print(count)

    a = np.arange(np.datetime64('2011-07-11'), np.datetime64('2011-07-18'))
    print(np.count_nonzero(np.is_busday(a)))

    # custom weekmasks
    # weekmask = [1, 1, 1, 1, 1, 0, 0]
    # weekmask = '1111100'
    # weekmask = 'Mon Tue Wed Thu Fri'
    # weekmask = 'MonTue Wed Thu\tFri'


if __name__ == '__main__':
    main()
