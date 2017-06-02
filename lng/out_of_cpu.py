# -*- coding: utf-8 -*-
import multiprocessing
import threading


def loop():
    x = 0
    while True:
        x = x ^ 1


def main():
    for i in range(multiprocessing.cpu_count()):
        print('cpu : {0}'.format(i))
        t = threading.Thread(target=loop)
        t.start()


if __name__ == '__main__':
    main()
