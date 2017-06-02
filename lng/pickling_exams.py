# -*- coding: utf-8 -*-
import pickle
import os


def main():
    d = dict(name='Bob', age=20, score=88)
    print(pickle.dumps(d))

    dump_file = os.path.join('data', 'dump.txt')
    with open(dump_file, 'wb') as f:
        pickle.dump(d, f)
    with open(dump_file, 'rb') as f:
        print(pickle.load(f))


if __name__ == '__main__':
    main()
