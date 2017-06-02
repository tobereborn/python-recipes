# -*- coding: utf-8 -*-
import os
from multiprocessing import Process


def test(name):
    print('Run child process {0}, pid {1}'.format(name, os.getpid()))


def main():
    print('Parent process is {0}'.format(os.getpid()))
    p = Process(target=test, args=('Joe',))
    print('Child process will run ....')
    p.start()
    p.join()
    print('Child process is finish')


if __name__ == '__main__':
    main()
