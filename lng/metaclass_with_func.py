#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""__metaclass__ is to create class,
the main purpose of a metaclass is to change the class automatically, when it's created.
"""


# example with meta function
def upper_attr(future_class_name, future_class_parent, future_class_attr):
    uppercase_attr = {}
    for name, val in future_class_attr.items():
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val
    return type(future_class_name, future_class_parent, uppercase_attr)


# this will affect all classes in the module
__metaclass__ = upper_attr


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
