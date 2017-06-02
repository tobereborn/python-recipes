#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29


class YieldIteratorExample:
    def __init__(self, seq):
        self.seq = seq
        self.iterator = self._next()
        self.next = self.iterator.next

    def _next(self):
        flag = 0
        for x in self.seq:
            if flag:
                flag = 0
                yield x
            else:
                flag = 1

    def __iter__(self):
        return self.iterator

    def refresh(self):
        self.iterator = self._next()
        self.next = self.iterator.next


def main():
    a = YieldIteratorExample('edcba')
    for x in a:
        print(x)
    print('­­­­­­­­­­')
    a.refresh()
    for x in a:
        print(x)
    print('=' * 30)
    a = YieldIteratorExample('abcde')
    try:
        print(a.next())
        print(a.next())
        print(a.next())
        print(a.next())
        print(a.next())
        print(a.next())
    except StopIteration as e:
        print('stopping', e)


if __name__ == '__main__':
    main()
