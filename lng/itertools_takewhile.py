# -*- coding: utf-8 -*-
import itertools


def main():
    natuals = itertools.count(1)
    ns = itertools.takewhile(lambda x: x <= 10, natuals)
    print(list(ns))


if __name__ == '__main__':
    main()
