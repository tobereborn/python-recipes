#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-6


def get_no_of_inst_with_cls(cls_obj):
    return cls_obj.no_inst


def get_no_of_inst_with_inst(inst_obj):
    return inst_obj.__class__.no_inst


class Kls(object):
    no_inst = 0

    def __init__(self, data):
        self.data = data
        Kls.no_inst += 1

    def pirntd(self):
        print self.data


def main():
    kls1 = Kls('abc')
    kls1.pirntd()
    print get_no_of_inst_with_cls(Kls)
    print get_no_of_inst_with_inst(kls1)
    kls2 = Kls('efg')
    kls2.pirntd()
    print get_no_of_inst_with_cls(Kls)
    print get_no_of_inst_with_inst(kls2)


if __name__ == '__main__':
    main()
