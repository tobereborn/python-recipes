# -*- coding: utf-8 -*-
from collections import namedtuple


def main():
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(1, 2)
    print('x = {0}, y = {1}'.format(p.x, p.y))
    print(isinstance(p, Point))
    print(isinstance(p, tuple))


if __name__ == '__main__':
    main()
