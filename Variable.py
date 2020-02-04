from _collections_abc import Iterable
from typing import Any


class VariableError(Exception):
    pass


class Variable:
    """
    This class represent a variable, with its associated domain.
    A Variable is immutable except for hidden value
    """
    def __init__(self, name: str, domain: Iterable):
        """
        :param name: variable's name
        :param domain: variable's domain (in any Iterable type)
        """
        self._name = name
        if isinstance(domain, Iterable):
            self._domain = set(domain)
        else:
            self._domain = set()
            self._domain.add(domain)
        self._hiddenValue = set()

    def getName(self) -> str:
        """
        :return: variable's name
        """
        return self._name

    def getInitialDomain(self) -> set:
        """
        :return: variable's domain, including hidden value
        """
        return self._domain.copy()

    def getActualDomain(self) -> set:
        """
        :return: variable's domain, excluding hidden values
        """
        return self._domain - self._hiddenValue

    def getActualDomainSize(self) -> int:
        """
        :return: variable's domain's size, excluding hidden values
        """
        return len((self._domain - self._hiddenValue))

    def validValue(self, value: Any) -> bool:
        """
        :param value: value to check for validity
        :return: True if value is in domain, False otherwise
        """
        if value in self._domain:
            return True
        else:
            return False

    def hideValue(self, value: Any) -> None:
        """
        Permits to hide a value from the variable's domain
        :param value: value to hide
        :return: None
        :raise VariableError: when the passed value doesn't exist in variable's domain
        """
        if value in self._domain:
            self._hiddenValue.add(value)
        else:
            raise VariableError

    def unhideValue(self, value: Any) -> None:
        """
        Permits to unhide a value from the variable's domain
        :param value: value to unhide
        :return: None
        :raise VariableError: when the passed value doesn't exist in variable's hidden values
        """
        if value in self._hiddenValue:
            self._hiddenValue.remove(value)
        else:
            raise VariableError

    def resetDomain(self) -> None:
        """
        Permits to unhide all hidden values from the variable's domain
        :return: None
        """
        self._hiddenValue.clear()
