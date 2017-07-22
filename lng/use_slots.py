# -*- coding: utf-8 -*-
#


class Student(object):
    __slots__ = ('name', 'age')


def set_age(self, age):
    self.age = age


def set_score(self, score):
    self.score = score


def main():
    s = Student()
    s.name = 'Michael'
    print(s.name)
    s.age = 25
    print(s.age)
    # s.score = 99
    # print(s.score)

    from types import MethodType
    s.set_age = MethodType(set_age, s)
    # s.set_age = set_age
    s.set_age(25)
    print(s.age)
    s2 = Student()
    # s2.set_age(25)
    # print(s2.age)

    Student.set_score = set_score
    s.set_score(100)
    print(s.score)
    s2.set_score(99)
    print(s2.score)


if __name__ == '__main__':
    main()
