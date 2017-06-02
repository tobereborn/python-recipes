# -*- coding: utf-8 -*-
from collections import defaultdict


def main():
    dd = defaultdict(lambda: 'N/A')
    dd['key1'] = 'abc'
    print(dd['key1'])
    print(dd['key2'])


if __name__ == '__main__':
    main()
