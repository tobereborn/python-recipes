# -*- coding: utf-8 -*-
import threading

banlance = 0


def main():
    lock = threading.Lock()

    def change_it(n):
        global banlance
        banlance += n
        banlance -= n

    def run_thread(n):
        for i in range(100000):
            try:
                lock.acquire()
                change_it(n)
            finally:
                lock.release()

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    print('..................')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('......****************.........')
    print(banlance)


if __name__ == '__main__':
    main()
