#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

class Node:
    def __init__(self, name='noname', value='novalue', children=None):
        self.name = name
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def iterchildren(self):
        for child in self.children:
            yield child
            # return self.children

    def walk(self, level=0):
        print '%sname: %s, value: %s' % (get_filter(level), self.get_name(), self.get_value())
        for child in self.iterchildren():
            child.walk(level + 1)


def walk(node, level=0):
    print '%sname: %s, value: %s' % (get_filter(level), node.get_name(), node.get_value())
    for child in node.iterchildren():
        walk(child, level + 1)


def get_filter(level):
    return '  ' * level


def main():
    a7 = Node('gilbert', '777')
    a6 = Node('fred', '666')
    a5 = Node('ellie', '555')
    a4 = Node('daniel', '444')
    a3 = Node('carl', '333', [a4, a5])
    a2 = Node('bill', '222', [a6, a7])
    a1 = Node('alice', '111', [a2, a3])
    # Use the walk method to walk the entire tree.
    print 'Using the method:'
    a1.walk()
    print '=' * 30
    # Use the walk function to walk the entire tree.
    print 'Using the function:'
    walk(a1)


if __name__ == '__main__':
    main()
