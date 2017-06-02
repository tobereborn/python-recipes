# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
import os, time, random


def write(q):
    print('Process to write: {0}'.format(os.getpid()))
    for value in ['A', 'B', 'C']:
        print('Put {0} to queue...'.format(value))
        q.put(value)
        time.sleep(random.random())


def read(q):
    print('Process to read: {0}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('Get {0} from queue'.format(value))


def main():
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    # force to terminate pr
    pr.terminate()


if __name__ == '__main__':
    main()
