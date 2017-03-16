#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


class Template(object):
    def __init__(self, user):
        self._user = user

    def language(self):
        pass

    def program(self):
        print('{0} is working on {1}'.format(self._user, self.language()))


class JavaWorker(Template):
    def __init__(self, user):
        super(JavaWorker, self).__init__(user)

    def language(self):
        return 'java'


class PythonWorker(Template):
    def __init__(self, user):
        super(PythonWorker, self).__init__(user)

    def language(self):
        return 'python'


def main():
    python = PythonWorker('tony')
    python.program()
    java = JavaWorker('jime')
    java.program()


if __name__ == '__main__':
    main()
