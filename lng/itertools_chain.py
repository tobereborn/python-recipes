# -*- coding: utf-8 -*-
import itertools


def main():
    for c in itertools.chain('ABC', 'XYZ'):
        print(c)


if __name__ == '__main__':
    main()
