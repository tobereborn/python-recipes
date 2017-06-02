# -*- coding: utf-8 -*-
from multiprocessing.managers import BaseManager
import queue, random, time


class QueueManager(BaseManager):
    pass


def main():
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)
    server_addr = '127.0.0.1'
    manager = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    manager.start()

    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(10):
        n = random.randint(0, 10000)
        print('put {0} in task'.format(n))
        task.put(n)

    print('try read task...')
    for i in range(10):
        print('{0}'.format(result.get(timeout=10)))

    manager.shutdown()
    print('end...')


if __name__ == '__main__':
    main()
