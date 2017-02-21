#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


def main():
    class ObjectCreator(object):
        pass

    my_object = ObjectCreator()
    print(my_object)

    # you can print a class since it is an object
    print(ObjectCreator)

    # you can pass a class as a parameter
    def echo(o):
        print(o)

    echo(ObjectCreator)
    print(hasattr(ObjectCreator, 'new_attr'))
    ObjectCreator.new_attr = 'foo'
    print(ObjectCreator.new_attr)

    # you can assign a class to a variable
    ObjectCreatorMirror = ObjectCreator
    print(ObjectCreatorMirror.new_attr)
    print(ObjectCreatorMirror())

    # create a class in a function using class keyword
    def choose_class(name):
        if name == 'foo':
            class Foo(object):
                pass

            return Foo
        elif name == 'bar':
            class Bar(object):
                pass

            return Bar

    MyClass = choose_class('foo')
    print(MyClass)
    print(MyClass())

    # create a class using type keyword
    # type( class name,
    #       tuple of parent classes,
    #       dict of attr names and values
    #      )
    MyShinyClass = type('MyShinyClass', (), {})
    print(MyShinyClass)
    print(MyShinyClass())
    Foo = type('Foo', (), {'bar': True})
    print(Foo)
    f = Foo()
    print(f)
    print(f.bar)
    FooChild = type('FooChild', (Foo,), {})
    print(FooChild)
    print(FooChild.bar)

    # add method
    def echo_bar(self):
        print('bar: %s' % self.bar)

    FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
    print(hasattr(Foo, 'echo_bar'))
    print(hasattr(FooChild, 'echo_bar'))
    my_foo = FooChild()
    my_foo.echo_bar()

    def echo_bar_more(self):
        print('yet another method')

    FooChild.echo_bar_more = echo_bar_more
    print(hasattr(FooChild, 'echo_bar_more'))

    # everything is object, which can be checked with __class__
    age = 35
    print(age.__class__)

    def foo():
        pass

    print(foo.__class__)

    class Bar(object):
        pass

    b = Bar()
    print(b.__class__)

    # __class of any __class__ is type , type is built-in meta class
    print (age.__class__.__class__)
    print(foo.__class__.__class__)
    print(b.__class__.__class__)


if __name__ == '__main__':
    main()
