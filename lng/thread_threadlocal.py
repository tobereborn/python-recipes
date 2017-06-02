# -*- coding: utf-8 -*-
import threading


def main():
    local_student = threading.local()

    def process_student():
        std = local_student.name
        print('************std = %s, and thread is %s' % (std, threading.current_thread().name))

    def process_test(name):
        local_student.name = name
        print('########local_student = %s, and thread is %s' % (local_student, threading.current_thread().name))
        process_student()

    print('test start ......')
    t1 = threading.Thread(target=process_test, args=('Joe',), name='Thread1')
    t2 = threading.Thread(target=process_test, args=('Cheer',), name='Thread2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('test end ......')


if __name__ == '__main__':
    main()
