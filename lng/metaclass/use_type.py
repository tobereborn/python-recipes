# -*- coding: utf-8 -*-
#


def fn(self, name='world'):
    print('Hello, {0}'.format(name))


def main():
    Hello = type('Hello', (object,), dict(hello=fn))
    h = Hello()
    print(h.hello())
    print(type(Hello))
    print(type(h))


if __name__ == '__main__':
    main()
