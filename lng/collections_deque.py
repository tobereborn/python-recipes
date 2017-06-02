# -*- coding: utf-8 -*-
from collections import deque


def main():
    q = deque(['a', 'b', 'c'])
    q.append('x')
    q.appendleft('y')
    print(q)
    print(q.pop())
    print(q)
    print(q.popleft())
    print(q)


if __name__ == '__main__':
    main()
