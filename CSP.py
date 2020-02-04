from __future__ import annotations

from typing import Set, Optional, List, Dict, Any
from copy import copy

from Variable import Variable
from Constraints import *
from Assignment import Assignment


class CSPError(Exception):
    pass


class CSP:
    """
    This class represent a Constraint Satisfaction Problem that can include unary and binary constraint.
    Between two variables can be defined only a single binary constraint.
    Between a variable and a value can be defined only a single unary constraint
    """
    def __init__(self):
        self._variables = set()
        self._unaryConstraints: Dict[Variable, Dict[Any, List[Constraint]]] = {}
        self._binaryConstraints: Dict[Variable, Dict[Variable, List[Constraint]]] = {}

    def __copy__(self):
        return self.subproblem(Assignment())

    def addVariable(self, var: Variable) -> None:
        """
        Adds a variable to the CSP
        :param var: variable to be add
        :return: None
        :raise CSPError: if var param is not a Variable
        """
        if not isinstance(var, Variable):
            raise CSPError

        self._variables.add(var)

    def getVariable(self, name: str) -> Variable:
        """
        Returns the variable with the name passed
        :param name: name of the variable
        :return: the variable with this name
        """
        for var in self._variables:
            if var.getName() == name:
                return var

    def getVariables(self) -> Set[Variable]:
        """
        :return: a defensive copy set with all variables
        """
        return self._variables.copy()

    def addUnaryConstraint(self, variable: Variable, constraint: Constraint, value, *, override: bool = False) -> None:
        """
        Adds a unary constraint to the CSP. The order of the variable is important!
        Isn't required to add also the dual constraint, that is added automatically
        :param variable: first variable
        :param constraint: constraint between the variables
        :param value: value
        :param override: when is setted to True, if already exist a constraint between this variable and this value, that will be overridden;
            if is setted to False, the constraint won't be added
        :return: None
        :raise CSPError: if variable or constraint params aren't respectively a Variable or a Constraint and
            if the variable doesn't exist in CSP's variables
        """
        if not isinstance(variable, Variable) or not isinstance(constraint, Constraint):
            raise CSPError

        if variable in self._variables:
            if variable not in self._unaryConstraints:
                self._unaryConstraints[variable] = {}
            if value not in self._unaryConstraints[variable]:
                self._unaryConstraints[variable][value] = []
            else:
                if not override:
                    return
                else:
                    self._unaryConstraints[variable][value].clear()      # if already exists a constraint with this value, delete it
            self._unaryConstraints[variable][value].append(constraint)
        else:
            raise CSPError

    def addBinaryConstraint(self, variable1: Variable, constraint: Constraint, variable2: Variable, *, override: bool = False) -> None:
        """
        Adds a binary constraint to the CSP. The order of the variable is important!
        Isn't required to add also the dual constraint, that is added automatically
        :param variable1: first variable
        :param constraint: constraint between the variables
        :param variable2: second variable
        :param override: when is setted to True, if already exist a constraint between these variables, that will be overridden;
            if is setted to False, the constraint won't be added
        :return: None
        :raise CSPError: if variables params aren't Variable and if they doesn't exist in CSP's variables
        """
        if not isinstance(variable1, Variable) or not isinstance(variable2, Variable) or not isinstance(constraint, Constraint):
            raise CSPError

        if variable1 in self._variables and variable2 in self._variables:
            if variable1 not in self._binaryConstraints:
                self._binaryConstraints[variable1] = {}
            if variable2 not in self._binaryConstraints:
                self._binaryConstraints[variable2] = {}
            if variable2 not in self._binaryConstraints[variable1]:
                self._binaryConstraints[variable1][variable2] = []
                self._binaryConstraints[variable2][variable1] = []
            else:
                if not override:
                    return
                else:
                    self._binaryConstraints[variable1][variable2].clear()   # if already exists a constraint between them, delete it
                    self._binaryConstraints[variable2][variable1].clear()
            self._binaryConstraints[variable1][variable2].append(constraint)
            self._binaryConstraints[variable2][variable1].append(constraint.getDual())
        else:
            raise CSPError

    def addAllDifferent(self) -> None:
        """
        Adds the different constraint between every couple of variables
        :return: None
        """
        for v1 in self._variables:
            for v2 in self._variables:
                if v1 is not v2:
                    self.addBinaryConstraint(v1, different, v2)

    def getBinaryConstraintsForVar(self, var: Variable) -> Dict[Variable, List[Constraint]]:
        """
        Returns all binary constraints that involve a variable
        :param var: variable to look for
        :return: dict for constraints
        :raise CSPError: if var param isn't a Variable
        """
        if var in self._variables:
            if var in self._binaryConstraints:
                return self._binaryConstraints[var]
            else:
                return {}
        else:
            raise CSPError

    def getUnaryConstraintsForVar(self, var: Variable) -> Dict[Any, List[Constraint]]:
        """
        Returns all unary constraints that involve a variable
        :param var: variable to look for
        :return: dict for constraints
        :raise CSPError: if var param isn't a Variable
        """
        if var in self._variables:
            if var in self._unaryConstraints:
                return self._unaryConstraints[var]
            else:
                return {}
        else:
            raise CSPError

    def findBinaryCostraint(self, var1: Variable, var2: Variable) -> Optional[Constraint]:
        """
        Returns the binary constraint existing between two variables
        :param var1:
        :param var2:
        :return: constraint if it exists or None otherwise
        """
        if var1 in self._binaryConstraints and var2 in self._binaryConstraints[var1]:
            return self._binaryConstraints[var1][var2][0]
        else:
            return None

    def findUnaryConstraint(self, var: Variable, value) -> Optional[Constraint]:
        """
        Returns the unary constraint existing between a variable and a value
        :param var:
        :param value:
        :return: constraint if it exists or None otherwise
        """
        if var in self._unaryConstraints and value in self._unaryConstraints[var]:
            return self._unaryConstraints[var][value][0]
        else:
            return None

    def getBinaryConstraints(self) -> dict:
        """
        :return: defensive copy of binary constraints
        """
        return self._binaryConstraints.copy()

    def getUnaryConstraints(self) -> dict:
        """
        :return: defensive copy of unary constraints
        """
        return self._unaryConstraints.copy()

    def getEdges(self) -> Set[tuple]:
        """
        Returns all tuples representing a constraint between two variables, including dual constraints
        :return: set of tuple
        """
        edges = set()
        for var1 in self._binaryConstraints:
            for var2 in self._binaryConstraints[var1]:
                edges.add((var1, var2))
        return edges

    def getNeighbour(self, var: Variable) -> Set[tuple]:
        """
        Returns all tuples representing a constraint between a variable and its neighbours
        :param var: variable to search for neighbour
        :return: set of tuple
        """
        edges = set()
        if var in self._binaryConstraints:
            for var2 in self._binaryConstraints[var]:
                edges.add((var, var2))
                edges.add((var2, var))
        return edges

    def countVariables(self) -> int:
        """
        :return: number of variables
        """
        return len(self._variables)

    def assignmentConsistency(self, assignment: Assignment) -> bool:
        """
        Check if an assignment is consistent or not
        :param assignment: assignment to check for consistency
        :return: True if it is consistent, False otherwise
        """
        assignment = assignment.getAssignment()
        for var in assignment:
            assignedValue = assignment[var]
            if assignedValue not in var.getActualDomain():
                return False
            if var in self._unaryConstraints:
                for value in self._unaryConstraints[var]:
                    if not self._unaryConstraints[var][value][0](assignedValue, value):
                        return False
            if var in self._binaryConstraints:
                for var2 in assignment:
                    if var2 is not var:
                        if var2 in self._binaryConstraints[var]:
                            if not self._binaryConstraints[var][var2][0](assignedValue, assignment[var2]):
                                return False
        return True

    def assignmentConsistencyForVar(self, assignment: Assignment, var: Variable) -> bool:
        """
        Check if a var assignment is consistent or not (in relation to other variable already assigned)
        :param assignment: assignment to check for consistency
        :param var: var to check for assignment
        :return: True if it is consistent, False otherwise
        """
        assignment = assignment.getAssignment()
        assignedValue = assignment[var]
        if assignedValue not in var.getActualDomain():
            return False
        if var in self._unaryConstraints:
            for value in self._unaryConstraints[var]:
                if not self._unaryConstraints[var][value][0](assignedValue, value):
                    return False
        if var in self._binaryConstraints:
            for var2 in assignment:
                if var2 is not var:
                    if var2 in self._binaryConstraints[var]:
                        if not self._binaryConstraints[var][var2][0](assignedValue, assignment[var2]):
                            return False
        return True

    def printActualDomains(self) -> None:
        """
        prints actual domain for all variables
        """
        for var in self._variables:
            print(var.getName() + ": " + str(var.getActualDomain()))

    def subproblem(self, assignment: Assignment, *, cheap: bool = False) -> CSP:
        """
        Given a (partial) assignment, it returns a csp with all unassigned variables and the new constraints to be satisfied in order to be consistent with original problem
        :param assignment: already assigned variables
        :param cheap: if True it doesn't set new unary constraint in order to save computation
        :return: sub-CSP
        """
        csp = CSP()
        assignment = assignment.getAssignment()
        for var in self._variables-assignment.keys():   # copy all remaining variables
            csp.addVariable(var)
        for var in set(self._unaryConstraints) & csp.getVariables():      # copy unary constraints involving remaining variables
            for value in self._unaryConstraints[var]:
                csp.addUnaryConstraint(var, self._unaryConstraints[var][value][0], value)
        for var in set(self._binaryConstraints) & csp.getVariables():     # copy binary constraints involving remaining variables
            for var2 in set(self._binaryConstraints[var]) & csp.getVariables():
                csp.addBinaryConstraint(var, self._binaryConstraints[var][var2][0], var2)

        if not cheap:
            for var in set(assignment.keys()) & self._binaryConstraints.keys():      # for every binary constraints involving assigned variable, add unary constraint for the other variable involved
                for var2 in set(self._binaryConstraints[var]) & csp.getVariables():
                    csp.addUnaryConstraint(var2, self._binaryConstraints[var][var2][0].getDual(), assignment[var])

        return csp

    def completeSubproblem(self, assignment: Assignment, sub: CSP) -> CSP:
        """
        Given a subproblem created with cheap method, it completes it adding new unary constraints in base to the assignment
        :param assignment: already assigned variables
        :param sub: subproblem
        :return: sub-CSP
        """
        assignment = assignment.getAssignment()
        for var in set(assignment.keys()) & self._binaryConstraints.keys():      # for every binary constraints involving assigned variable, add unary constraint for the other variable involved
            for var2 in set(self._binaryConstraints[var]) & sub.getVariables():
                sub.addUnaryConstraint(var2, self._binaryConstraints[var][var2][0].getDual(), assignment[var])
        return sub

    def adapt(self, var: Variable, value: Any, cheap: bool = False) -> None:
        """
        Given an assignment for a var, transforms the csp into a subproblem
        :param var: Variable assigned
        :param value: vale assigned
        """
        if var not in self._variables:
            raise CSPError

        self._variables.remove(var)
        self._unaryConstraints.pop(var, None)
        for var2 in self._binaryConstraints[var]:
            if not cheap:
                self.addUnaryConstraint(var2, self._binaryConstraints[var][var2][0].getDual(), value)
            self._binaryConstraints[var2].pop(var)
        self._binaryConstraints.pop(var, None)


class CSPWorkingCopy:
    def __init__(self, csp: CSP):
        self._csp = copy(csp)
        self._hiddenVars = set()

    def hideVar(self, var: Variable) -> None:
        if var not in self._csp.getVariables():
            raise CSPError

        self._hiddenVars.add(var)

    def unhideVar(self, var: Variable) -> None:
        if var not in self._csp.getVariables():
            raise CSPError

        self._hiddenVars.remove(var)

    def getEdges(self) -> Set[tuple]:
        """
        Returns all tuples representing a constraint between two variables, including dual constraints
        :return: set of tuple
        """
        edges = set()
        for var1 in self._csp.getBinaryConstraints():
            if var1 not in self._hiddenVars:
                for var2 in self._csp.getBinaryConstraintsForVar(var1):
                    if var2 not in self._hiddenVars:
                        edges.add((var1, var2))
        return edges

    def countNeighbours(self, var: Variable) -> int:
        """
        :param var: var to search for neighbours
        :return: number of not hidden neighbours of var
        """
        count = 0
        for var in self._csp.getBinaryConstraintsForVar(var).keys():
            if var not in self._hiddenVars:
                count += 1
        return count

    def getVariables(self) -> Set[Variable]:
        return self._csp.getVariables() - self._hiddenVars
