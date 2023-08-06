"""
This file contains code for the Python library "TriplePair".
Author: GlobalCreativeApkDev
"""

# Importing necessary libraries.


import copy
from mpmath import mp, mpf

mp.pretty = True


# Creating static function to check whether an object is a number or not


def is_number(obj: object) -> bool:
    try:
        mpf(str(obj))
        return True
    except ValueError:
        return False


# Creating necessary class.


class TriplePair:
    """
    This class contains attributes of a TriplePair in Python.
    """

    def __init__(self, left, middle, right):
        # type: (object, object, object) -> None
        self.left: object = left
        self.middle: object = middle
        self.right: object = right

    def zip(self, other):
        # type: (TriplePair) -> TriplePair
        left = (self.left, other.left)
        middle = (self.middle, other.middle)
        right = (self.right, other.right)
        return TriplePair(left, middle, right)

    def sum(self, other):
        # type: (TriplePair) -> TriplePair
        if not is_number(self.left) or not is_number(other.left) \
                or not is_number(self.middle) or not is_number(other.middle) \
                or not is_number(self.right) or not is_number(other.right):
            raise Exception("Sum is not applicable since not all triple pair values are numbers.")
        return TriplePair(mpf(self.left) + mpf(other.left), mpf(self.middle) + mpf(other.middle),
                          mpf(self.right) + mpf(other.right))

    def __eq__(self, other):
        # type: (object) -> bool
        if not issubclass(TriplePair, type(other)):
            return False
        return self.left == other.left and self.middle == other.middle and self.right == other.right

    def __str__(self):
        # type: () -> str
        return "(" + str(self.left) + ", " + str(self.middle) + ", " + str(self.right) + ")"

    def clone(self):
        # type: () -> TriplePair
        return copy.deepcopy(self)
