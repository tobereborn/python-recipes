#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-7


def tag_wrap(tag):
    def decorator(fn):
        def inner(s):
            return r'<%s>%s<\%s>' % (tag, fn(s), tag)

        return inner

    return decorator


@tag_wrap('b')
@tag_wrap('em')
def greet(name):
    return 'Hello %s' % name


def main():
    print(greet('Girl'))


if __name__ == '__main__':
    main()
