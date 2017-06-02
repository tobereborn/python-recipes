# -*- coding: utf-8 -*-
from io import BytesIO


def test_get_value():
    f = BytesIO()
    f.write('zhong wen'.encode('utf-8'))
    print(f.getvalue())


def test_read_line():
    f = BytesIO(b'hello hello hi hi hi')
    print(f.read())


def main():
    test_get_value()
    test_read_line()


if __name__ == '__main__':
    main()
