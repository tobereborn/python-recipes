# -*- coding: utf-8 -*-
from multiprocessing.managers import BaseManager
import queue, time


class QueueManager(BaseManager):
    pass


def main():
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    server_addr = '127.0.0.1'
    print('Connect to server {0}...'.format(server_addr))
    manager = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    manager.connect()

    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(10):
        try:
            n = task.get(timeout=1)
            print('run task {0}*{1}...'.format(n, n))
            r = '{0}*{1}={2}'.format(n, n, n * n)
            time.sleep(1)
            result.put(r)
        except queue.Empty:
            print('task queue is empty.')
    print('end...')


if __name__ == '__main__':
    main()
