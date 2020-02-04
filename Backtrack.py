from typing import Union

from CSP import *
from AC3 import AC3


def orderVariables(csp: CSP, assignment: Assignment) -> Variable:
    """
    Given a csp and an assignment, selects unassigned variable ordered following Minimum Remaining Values and Degree Heuristic
    :param csp: the csp
    :param assignment: partial assignment
    :return: first variable
    """
    varAssignment: Dict[Variable] = assignment.getAssignment()
    unassigned = [var for var in list(csp.getVariables() - varAssignment.keys())]
    unassigned.sort(key=lambda var: ((var.getActualDomainSize() - len(assignment.getInferencesForVar(var))), -len(csp.getBinaryConstraintsForVar(var))))
    return unassigned[0]


def orderDomainValues(csp: CSP, assignment: Assignment, var: Variable) -> List:
    """
    Orders the remaining values from a variable's domain following Least Constraining Value (minimum number of crossouts)
    :param csp: the csp from which variable is extract
    :param assignment: partial assignment
    :param var: variable of interest
    :return: list of values
    """

    def countCrossout(var1: Variable, value: Any) -> int:
        count = 0
        for var2 in csp.getBinaryConstraintsForVar(var1):
            for value2 in var2.getActualDomain():
                if not csp.findBinaryCostraint(var1, var2)(value, value2):
                    count += 1
        return count

    values = list(var.getActualDomain() - assignment.getInferencesForVar(var))
    values.sort(key=lambda value: countCrossout(var, value))        # Least Constraining Value
    return values


def MAC(csp: CSP, assignment: Assignment, s: Set[tuple]) -> bool:
    """
    Maintaining Arc Consistency
    Check if, given a partial assignment, is possible to complete it satisfying all constraints. It is an AC-3 modified
    :param csp: the csp
    :param assignment: partial assignment
    :param s: starting set of edges
    :return: True if it's possible to complete the assignment, False if not
    """

    def revise(varI_i: Variable, constraint_i: Constraint, varJ_i: Variable, assignment_i: Assignment) -> bool:
        """
        Check for every value in the first variable's domain (or the assigned value) if exist a value of neighbour's domain compatible with it;
        if it doesn't exist, the value will be hidden using assignment's inference feature, instead of a definitive variable's hidden value
        :param varI_i: first variable
        :param constraint_i: constraint between the variables
        :param varJ_i: second variable
        :param assignment_i: partial assignment
        :return: True if the domain has been reduced, False otherwise
        """
        revised = False

        inferences = assignment_i.getInferences()
        varAssignment = assignment_i.getAssignment()
        if varI_i in varAssignment:       # if var has been assigned, we check for that value...
            valuesI = [varAssignment[varI_i]]
        else:       # ... else for all actual values in domain
            valuesI = varI_i.getActualDomain()
            if varI_i in inferences:
                valuesI -= inferences[varI_i]
        if varJ_i in varAssignment:       # if var has been assigned, we check for that value...
            valuesJ = [varAssignment[varJ_i]]
        else:       # ... else for all actual values in domain
            valuesJ = varJ_i.getActualDomain()
            if varJ_i in inferences:
                valuesJ -= inferences[varJ_i]

        for valueX in valuesI:          # for all the values to be checked...
            for valueY in valuesJ:          # we control all the values possible in second variable's actual domain
                if constraint_i(valueX, valueY):
                    break
            else:
                assignment_i.addVarInferenced(varI_i, valueX)       # if none is compatible, then we hide the value
                revised = True
        return revised

    while len(s) is not 0:
        edge = s.pop()          # Take an edge...
        constraint = csp.findBinaryCostraint(edge[0], edge[1])
        varI = edge[0]
        varJ = edge[1]
        if varI not in assignment.getAssignment().keys() or varJ not in assignment.getAssignment().keys():        # we'll do inference only if at least one of the variables has not been assigned
            if revise(varI, constraint, varJ, assignment):          # ... and analise the relative constraint. If has been made inference, we have to check something
                if len(varI.getActualDomain() - assignment.getInferencesForVar(varI)) == 0:        # If a domain is empty, the csp is unsatisfiable
                    return False
                otherConstraints = csp.getBinaryConstraintsForVar(varI)       # get others constraints involving inferenced variable...
                otherEdges = set()
                for var in otherConstraints:
                    if var != varJ:
                        otherEdges.add((var, varI))         # ... convert them to edges ...
                s = s.union(otherEdges)         # ... and add them to the set of edges to analise
    return True


def backtrack(csp: CSP) -> Assignment:
    """
    Given a csp, find a possible assignment
    Execution time: O(n^d) d=max cardinality
    :param csp: csp of interest
    :return: assignment that satisfies the csp, eventually null if it is unsatisfiable
    """

    def backtrackSearch(csp_i: CSP, assignment_i: Assignment = None) -> Optional[Assignment]:
        """
        Executes backtracking search for a complete assignment of a csp
        :param csp_i: csp of interest
        :param assignment_i: eventual partial assignment to respect
        :return: assignment if it exist, None otherwise
        """
        if assignment_i is None:      # if it's the init call, we run AC-3 and we initialize an assignment
            if not AC3(csp_i):
                return None
            assignment_i = Assignment()

        if len(assignment_i.getAssignment()) == csp_i.countVariables():     # if the assignment is complete, we can return it
            return assignment_i

        var = orderVariables(csp_i, assignment_i)
        values = orderDomainValues(csp_i, assignment_i, var)

        for value in values:
            localAssignment = copy(assignment_i)            # we try to assign a var in a local copy of assignment
            localAssignment.addVarAssigned(var, value)
            if MAC(csp_i, localAssignment, csp_i.getNeighbour(var)):      # if it's possible to complete the assignment, we iterate...
                result = backtrackSearch(csp_i, localAssignment)
                if result is not None:      # ... if it fails, we go back and propagate the None result
                    return result   # if the recursion arrive to a None, we don't want to propagate it, but we want to try next value
        return None

    assignment = backtrackSearch(csp)
    if assignment is None:
        nullAssignment = Assignment()
        nullAssignment.setNull()
        return nullAssignment
    return assignment


def allSolutions(csp: CSP, *, count: bool = False, assignment: Assignment = None, solutions: Union[List[Assignment], int] = None) -> Union[List[Assignment], int]:
    """
    Executes a modified backtracking search for all complete assignment of a csp.
    Execution time: Theta(n^d) d=max cardinality. ONLY FOR TEST PURPOSE
    :param count: if you want only count the number of solution set it to True
    :param csp: csp of interest
    :param assignment: eventual partial assignment to respect
    :param solutions: eventual already found solutions
    :return: assignment if it exist, None otherwise
    """
    if assignment is None:  # if it's the init call, we run AC-3 and we initialize an assignment
        AC3(csp)
        assignment = Assignment()

    if solutions is None:
        if count:
            solutions = 0
        else:
            solutions = []

    unassigned = [var for var in list(csp.getVariables() - assignment.getAssignment().keys())]
    var = unassigned[0]
    values = list(var.getActualDomain() - assignment.getInferencesForVar(var))
    for value in values:
        localAssignment = copy(assignment)        # we try to assign a var in a local copy of assignment
        localAssignment.addVarAssigned(var, value)
        if csp.assignmentConsistency(localAssignment):
            if len(localAssignment.getAssignment()) == csp.countVariables():        # if the assignment is complete and consistent, we can store it
                if count:
                    solutions += 1
                else:
                    solutions.append(localAssignment)
            else:
                if count:
                    solutions = allSolutions(csp, count=count, assignment=localAssignment, solutions=solutions)
                else:
                    allSolutions(csp, count=count, assignment=localAssignment, solutions=solutions)

    return solutions
