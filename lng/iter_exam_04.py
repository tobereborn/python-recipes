#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29


class IteratorExample:
    def __init__(self, seq):
        self.seq = seq
        self.idx = 0

    def next(self):
        self.idx += 1
        if self.idx >= len(self.seq):
            raise StopIteration
        value = self.seq[self.idx]
        self.idx += 1
        return value

    def __iter__(self):
        return self

    def refresh(self):
        self.idx = 0


def main():
    a = IteratorExample('edcba')
    for x in a:
        print(x)
    print('­­­­­­­­­­')
    a.refresh()
    for x in a:
        print(x)
    print('=' * 30)
    a = IteratorExample('abcde')
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
