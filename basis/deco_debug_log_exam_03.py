#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


def log_calls(fn):
    """ Wraps fn in a function named "inner" that writes
            the arguments and return value to logfile.log """

    def inner(*args, **kwargs):
        out = apply(fn, args, kwargs)
        with open('logfile.log', 'a') as f:
            f.write('%s calls with args %s kwargs %s, returning %s\n' % (fn.__name__, args, kwargs, out))
        return out

    return inner


@log_calls
def fizz_buzz_or_number(i):
    if i % 15 == 0:
        return 'fizzbuzz'
    elif i % 3 == 0:
        return 'fizz'
    elif i % 5 == 0:
        return 'buzz'
    else:
        return i


def main():
    fizz_buzz_or_number(1)
    fizz_buzz_or_number(2)
    fizz_buzz_or_number(3)
    fizz_buzz_or_number(5)


if __name__ == '__main__':
    main()
