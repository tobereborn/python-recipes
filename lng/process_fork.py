# -*- coding: utf-8 -*-
import os, time


def main():
    source = 10
    pid = os.fork()
    if pid == 0:
        time.sleep(20)
        print('Child process n = %d' % (source - 1))
    else:
        print('Parent process n = %d' % source)


if __name__ == '__main__':
    main()
