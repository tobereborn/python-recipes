# -*- coding: utf-8 -*-
import os
import time
import random
from multiprocessing import Pool


def test(arg):
    print('Run child process: arg = {0}, pid = {1}'.format(arg, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 2)
    end = time.time()
    print('Pid = {0}, time = {1:0.2f}'.format(os.getpid(), end - start))


def main():
    pool = Pool(4)
    for i in range(5):
        pool.apply_async(test, args=(i,))
    print('Wait all subprocess done')
    pool.close()
    pool.join()
    print('Closed')


if __name__ == '__main__':
    main()
