#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""__metaclass__ is to create class,
the main purpose of a metaclass is to change the class automatically, when it's created.
"""


class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, dict):
        uppercase_attr = {}
        for name, val in dict.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        # cls works the way as self
        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, dict)
        # or return type.__new__(cls, clsname, bases, uppercase_attr)


__metaclass__ = UpperAttrMetaclass



class Foo():
    # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'


def main():
    print(hasattr(Foo, 'bar'))
    print(hasattr(Foo, 'BAR'))
    f = Foo()
    print(f.BAR)


if __name__ == '__main__':
    main()
