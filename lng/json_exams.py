# -*- coding: utf-8 -*-
import json


def test_basic():
    d1 = dict(name='Bod', age=20, score=88)
    print('dict: {0}'.format(d1))
    json_str = json.dumps(d1)
    print('dict to json: {0}'.format(json_str))
    d2 = json.loads(json_str)
    print('json to dict: {0}'.format(d2))


class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


def test_class():
    s1 = Student('Bob', 20, 88)
    json_str = json.dumps(s1, default=student2dict)
    # json_str = json.dumps(s1, default=lambda obj: obj.__dict__)
    print('class to json: {0}'.format(json_str))
    s2 = json.loads(json_str, object_hook=dict2student)
    print('json to class : {0}'.format(s2))


def main():
    test_basic()
    test_class()


if __name__ == '__main__':
    main()
