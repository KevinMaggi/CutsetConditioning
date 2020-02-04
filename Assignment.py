from __future__ import annotations

from Variable import Variable
from typing import Any, Dict, Set
from copy import copy


class AssignmentError(Exception):
    pass


class Assignment:
    """
    This class represent an assignment.
    It contains also value to be hidden from other variable after an assignment and the inference
    An assignment is null if its attribute "null" is true
    """
    def __init__(self):
        self._assignment: Dict[Variable, Any] = {}
        self._inferences: Dict[Variable, Set] = {}
        self._null: bool = False

    def __copy__(self):
        """
        Defensive copy
        """
        newAssignment = Assignment()
        for var in self._assignment:
            newAssignment.addVarAssigned(var, self._assignment[var])
        for var in self._inferences:
            for value in self._inferences[var]:
                newAssignment.addVarInferenced(var, value)
        return newAssignment

    def __add__(self, other: Assignment) -> Assignment:
        """
        Add method for assignment. Only the assigned variable will be united, the inferences will be ignored
        """
        newAssignment = Assignment()
        for var in self._assignment:
            newAssignment.addVarAssigned(var, self._assignment[var])
        for var in other.getAssignment():
            newAssignment.addVarAssigned(var, other.getAssignment()[var])
        return newAssignment

    def setNull(self) -> None:
        """
        Set the assignment as null
        """
        self._null = True
        self._assignment.clear()
        self._inferences.clear()

    def isNull(self) -> bool:
        """
        get the nullity of assignment
        """
        return self._null

    def addVarAssigned(self, var: Variable, value: Any) -> None:
        """
        Adds an assignment for variable
        :param var: variable to be assigned
        :param value: value to be assigned
        """
        if self._null:
            raise AssignmentError
        if not isinstance(var, Variable):
            raise AssignmentError

        if var.validValue(value):
            self._assignment[var] = value
        else:
            raise AssignmentError

    def removeVarAssigned(self, var: Variable) -> None:
        """
        Removes an assignment for variable
        :param var: variable to be removed
        """
        if self._null:
            raise AssignmentError
        if not isinstance(var, Variable):
            raise AssignmentError

        self._assignment.pop(var)

    def getAssignment(self) -> Dict[Variable, Any]:
        """
        :return: defensive copy of assignment's values
        """
        return self._assignment.copy()

    def addVarInferenced(self, var: Variable, value: Any) -> None:
        """
        Adds a value to be hidden from a variable, after an assignment
        :param var: variable to hide
        :param value: value to hide
        """
        if self._null:
            raise AssignmentError
        if not isinstance(var, Variable):
            raise AssignmentError

        if var.validValue(value):
            if var not in self._inferences:
                self._inferences[var] = set()
            self._inferences[var].add(value)
        else:
            raise AssignmentError

    def getInferencesForVar(self, var: Variable) -> Set:
        """
        Returns all the hidden values for a variable
        :param var: variable to search for hidden values
        :return: hidden values
        """
        if not isinstance(var, Variable):
            raise AssignmentError

        if var in self._inferences:
            return self._inferences[var].copy()
        else:
            return set()

    def getInferences(self) -> Dict[Variable, Set]:
        """
        :return: defensive copy of hidden values
        """
        return self._inferences.copy()

    def printAssignment(self) -> None:
        """
        Prints the assignment
        """
        if self._null:
            print('null assignment')
            return
        for var in self._assignment:
            print(var.getName() + ": " + str(self._assignment[var]))
        if len(self._assignment) == 0:
            print('empty assignment')
