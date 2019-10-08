import unittest

from app.base.loggerNoSQL import loggerNoSQL

l1 = loggerNoSQL()

l1.newLog('message of Today 1', "ERROR", "Tests", 1)

class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val


def test_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    try:
        assert f1 == f2
    except AssertionError as ae:
        print(ae)

#test_compare()