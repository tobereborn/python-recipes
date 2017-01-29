#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by weizhenjin on 17-1-29

import sys,unittest

class MyTest(unittest.TestCase):
    def test_one(self):
        print 'test one'

    def test_two(self):
        print 'test two'


def suite():
    loader= unittest.TestLoader()
    testsuite=loader.loadTestsFromTestCase(MyTest)
    return testsuite

def test():
    testsuite=suite()
    runner=unittest.TextTestRunner(sys.stdout,verbosity=2)
    result=runner.run(testsuite)


if __name__ == '__main__':
    test()