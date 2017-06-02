# -*- coding: utf-8 -*-
import itertools


def main():
    for key, group in itertools.groupby('AaaBbaaaaaBcCaAA', lambda c: c.upper()):
        print(key, list(group))


if __name__ == '__main__':
    main()
