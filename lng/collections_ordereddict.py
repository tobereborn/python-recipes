# -*- coding: utf-8 -*-
from collections import OrderedDict


class LastUpdateOrderedDict(OrderedDict):
    def __init__(self, capacity):
        super(LastUpdateOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        contains_key = 1 if key in self else 0
        if len(self) - contains_key >= self._capacity:
            last = self.popitem(last=False)
            print('remove: ', last)
        if contains_key:
            del self[key]
            print('set:', (key, value))
        else:
            print('add: ', (key, value))
        OrderedDict.__setitem__(self, key, value)


def main():
    d = dict([('b', 2), ('a', 1), ('c', 3)])
    print(d)
    od = OrderedDict([('b', 2), ('c', 3), ('a', 1)])
    print(list(od.keys()))


if __name__ == '__main__':
    main()
