# -*- coding: utf-8 -*-
from io import StringIO


def test_get_value():
    f = StringIO()
    f.write('hello')
    f.write(' ')
    f.write('world!')
    print(f.getvalue())


def test_read_line():
    f = StringIO('Hello!\nHi!\nGoodbye!')
    while True:
        s = f.readline()
        if s == '':
            break
        print(s.strip())


def main():
    test_get_value()
    test_read_line()

if __name__ == '__main__':
    main()
