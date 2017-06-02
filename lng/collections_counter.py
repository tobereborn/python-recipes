# -*- coding: utf-8 -*-
from collections import Counter


def main():
    c = Counter()
    for ch in 'programming':
        c[ch] += 1
    print(c)

if __name__ == '__main__':
    main()
