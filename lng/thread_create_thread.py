# -*- coding: utf-8 -*-
import threading, time


def test():
    print('1-----thread is {0}'.format(threading.current_thread().name))
    n = 0
    while n < 10:
        n += 1
        print('2-----thread is {0}'.format(threading.current_thread().name))
        time.sleep(3)


def main():
    print('3-----thread is {0}'.format(threading.current_thread().name))
    print('4-----thread is {0}'.format(threading.current_thread().name))
    thread = threading.Thread(target=test, name='testLoop')
    print('5-----thread is {0}'.format(threading.current_thread().name))
    thread.start()
    thread.join()
    print('6-----thread is {0}'.format(threading.current_thread().name))


if __name__ == '__main__':
    main()
