#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Foo(object):
    x = 1

    @classmethod
    def show(cls):
        print('foo class:{0}'.format(cls.x))


class Bar(Foo):
    x = 2

    # @classmethod
    # def show(cls):
    #     print('bar class:{0}'.format(cls.x))


def main():
    bar = Bar()
    bar.show()


if __name__ == '__main__':
    main()
