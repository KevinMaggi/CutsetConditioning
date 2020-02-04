from __future__ import annotations

from typing import Callable
from inspect import signature


class ConstraintError(Exception):
    pass


class Constraint:
    """
    This class represent a constraint, substantially a function wrapper with some additional features.
    A Constraint is immutable
    """
    def __init__(self, function: Callable[..., bool], dual: bool = False):
        """
        :param function: function that represent the constraint; it should accept exactly 2 params and return a bool
        :param dual: typically a constraint isn't commutative, if this param is setted to True, indicates that the constraint is the inverse of the function
        :raise ConstraintError: if the passed function doesn't accept exactly 2 params or it isn't a Callable
        """
        if not isinstance(function, Callable):
            raise ConstraintError
        self._function = function
        self._cardinality = 2
        self._dual: bool = dual
        if len(signature(self._function).parameters) != self._cardinality:
            raise ConstraintError

    def __call__(self, value1, value2) -> bool:
        """
        Executes the function constraint passing it the value. If it is a dual constraint, the values will be swapped
        :param value1:
        :param value2:
        :return: a boolean that indicates if the constraint is respected by these values or not
        """
        if self._dual:
            value1, value2 = value2, value1
        return self._function(value1, value2)

    def getType(self) -> Callable:
        """
        Returns the function inside the constraint
        :return: constraint's function
        """
        return self._function.__name__

    def getDual(self) -> Constraint:
        """
        returns the inverse constraint
        :return: inverse constraint
        """
        return Constraint(self._function, not self._dual)


def equals(a, b) -> bool:
    """
    Predefined function constraint: check if two values are equal
    :param a:
    :param b:
    :return: True if a==b, False otherwise
    """
    if a == b:
        return True
    else:
        return False


def different(a, b) -> bool:
    """
    Predefined function constraint: check if two values are different
    :param a:
    :param b:
    :return: True if a!=b, False otherwise
    """
    return not equals(a, b)


def greater(a, b) -> bool:
    """
    Predefined function constraint: check if a value is greater than another
    :param a:
    :param b:
    :return: True if a>b, False otherwise
    """
    if a > b:
        return True
    else:
        return False


def greaterOrEqual(a, b) -> bool:
    """
    Predefined function constraint: check if a value is greater than or equal to another
    :param a:
    :param b:
    :return: True if a>=b, False otherwise
    """
    if a >= b:
        return True
    else:
        return False


def lesser(a, b) -> bool:
    """
    Predefined function constraint: check if a value is lesser than another
    :param a:
    :param b:
    :return: True if a<b, False otherwise
    """
    return not greaterOrEqual(a, b)


def lesserOrEqual(a, b) -> bool:
    """
    Predefined function constraint: check if a value is lesser than or equal to another
    :param a:
    :param b:
    :return: True if a<=b, False otherwise
    """
    return not greater(a, b)
