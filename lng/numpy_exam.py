#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-14

# http://codingpy.com/article/an-introduction-to-numpy/

import numpy as np


def main():
    a = np.array([0, 1, 2, 3, 4])
    b = np.array((0, 1, 2, 3, 4))
    c = np.arange(5)
    d = np.linspace(0, 2 * np.pi, 5)
    print(a)
    print(b)
    print(c)
    print(d)
    e = np.array([[11, 12, 13, 14, 15],
                  [16, 17, 18, 19, 20],
                  [21, 22, 23, 24, 25],
                  [26, 27, 28, 29, 30],
                  [31, 32, 33, 34, 35]
                  ])
    print(e)
    print(e[2, 4])
    print(e[0, 1:4])
    print(e[1:4, 0])
    print(e[::2, ::2])
    print(e[:, 1])
    print(type(a))
    print(e.dtype)
    print(e.size)
    print(e.shape)
    print(e.itemsize)
    print(e.ndim)
    print(e.nbytes)
    f = np.arange(25)
    print(f)
    f = f.reshape(5, 5)
    print('f: \n%s' % f)
    h = np.array([10, 62, 1, 14, 2, 56, 79, 2, 1, 45,
                  4, 92, 5, 55, 63, 43, 35, 6, 53, 24,
                  56, 3, 56, 44, 78])
    print(h)
    h = h.reshape(5, 5)
    print("h: \n%s" % h)
    print(f + h)
    print(f - h)
    print('f*h: \n%s' % (f * h))
    print(f / h)
    print('f**2: \n%s' % f ** 2)
    print(f < h)
    print(f > h)
    print(f.dot(h))
    i = np.arange(10)
    print('i: \n%s' % i)
    print(i.sum())
    print(i.min())
    print(i.max())
    print(i.cumsum())
    j = np.arange(0, 100, 10)
    print('j: \n%s' % j)
    indices = [1, 5, -1]
    k = j[indices]
    print(k)

    import matplotlib.pyplot as plt
    l = np.linspace(0, 2 * np.pi, 50)
    print('l: \n%s' % l)
    m = np.sin(l)
    plt.plot(l, m)
    mask = m >= 0
    plt.plot(l[mask], m[mask], 'bo')
    mask = (m >= 0) & (l <= np.pi / 2)
    plt.plot(l[mask], m[mask], 'go')
    plt.show()
    n = np.arange(0, 100, 10)
    o = n[:5]
    p = n[n >= 50]
    print(o)
    print(p)
    q = np.arange(0, 100, 10)
    r = np.where(q < 50)
    s = np.where(q >= 50)[0]
    print(r)
    print(s)
    print(np.arange(10000).reshape(100, 100))
    print(np.zeros((3, 4)))
    print(np.ones((2, 3), dtype=np.int16))
    print(np.empty((2, 3)))


if __name__ == '__main__':
    main()
