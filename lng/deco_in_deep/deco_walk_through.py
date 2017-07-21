# -*- coding: utf-8 -*-


#  ---------------------------Passing arguments to the decorated function
def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print("I got args! Look: {0}, {1}".format(arg1, arg2))
        function_to_decorate(arg1, arg2)

    return a_wrapper_accepting_arguments


@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print('My name is {0} {1}'.format(first_name, last_name))


# ------------------------------Decorating methods
def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie -= 3  # very friendly, decrease age even more :-)
        return method_to_decorate(self, lie)

    return wrapper


class Lucy(object):
    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def sayYourAge(self, lie):
        print("I am {0}, what did you think?".format(self.age + lie))


def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # The wrapper accepts any arguments
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print("Do I have args?:")
        print(args)
        print(kwargs)
        # Then you unpack the arguments, here *args, **kwargs
        # If you are not familiar with unpacking, check:
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        function_to_decorate(*args, **kwargs)

    return a_wrapper_accepting_arbitrary_arguments


@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print("Python is cool, no argument here.")


@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)


@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Why not ?"):
    print("Do {0}, {1} and {2} like platypus? {3}".format(a, b, c, platypus))


class Mary(object):
    def __init__(self):
        self.age = 31

    @a_decorator_passing_arbitrary_arguments
    def sayYourAge(self, lie=-3):  # You can now add a default value
        print("I am {0}, what did you think?".format(self.age + lie))


# ------------------------------ with arguments ------------------------
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):
    print("I make decorators! And I accept arguments: {0}, {1}".format(decorator_arg1, decorator_arg2))

    def my_decorator(func):
        # The ability to pass arguments here is a gift from closures.
        # If you are not comfortable with closures, you can assume it’s ok,
        # or read: https://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print("I am the decorator. Somehow you passed me arguments: {0}, {1}".format(decorator_arg1, decorator_arg2))

        # Don't confuse decorator arguments and function arguments!
        def wrapped(function_arg1, function_arg2):
            print("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator


@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print("I am the decorated function and only knows about my arguments: {0}"
          " {1}".format(function_arg1, function_arg2))


def main():
    print_full_name("Peter", "Venkman")
    l = Lucy()
    l.sayYourAge(-3)
    function_with_no_argument()
    function_with_arguments(1, 2, 3)
    function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
    m = Mary()
    m.sayYourAge()
    decorated_function_with_arguments("Rajesh", "Howard")


if __name__ == '__main__':
    main()
