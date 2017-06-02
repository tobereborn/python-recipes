# -*- coding: utf-8 -*-
import os


def main():
    print(os.name)
    print(os.uname())
    print(os.environ)
    print(os.environ.get('PATH'))
    print(os.path.abspath('/home/root/test/../'))
    print(os.path.join('/homw/root', 'test'))
    if not os.path.exists('data/testdir'):
        os.mkdir('data/testdir')
    os.rmdir('data/testdir')
    print(os.path.split('/home/root/test'))
    print(os.path.splitext('/home/root/test.txt'))


if __name__ == '__main__':
    main()
