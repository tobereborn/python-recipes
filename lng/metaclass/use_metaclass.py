# -*- coding: utf-8 -*-
#


class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)


class MyList(list, metaclass=ListMetaclass):
    pass


def main():
    l1 = MyList()
    l1.add(5)
    print(l1)
    l2 = list()
    # l2.add(1)
    print(l2)


if __name__ == '__main__':
    main()
