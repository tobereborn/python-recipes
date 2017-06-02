# -*- coding: utf-8 -*-
import itertools


def main():
    cs = itertools.cycle('ABC')
    for c in cs:
        print(c)


if __name__ == '__main__':
    main()
