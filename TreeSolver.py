from typing import Union

from AC3 import revise
from CSP import *


def topSort(csp: CSP, root: Variable) -> List[Variable]:
    """
    Given a csp, it searches for a "topological sort" (running a DFS). It needs a variable from which starting, because induced graph isn't a direct graph, so
    the real topological sort isn't defined
    :param csp: csp of interest
    :param root: variable from which it starts
    :return: Order list of csp's variables
    :raise Exception: if the graph induced isn't a tree (it is cyclic or not connected)
    """

    def _topSort(csp_i: CSP, root_i: Variable, previous: List[Variable]) -> List[Variable]:
        """
        Adds to the list the subroot and iterates
        :param csp_i:  csp of interest
        :param root_i: variable from which it starts
        :param previous: already elaborated nodes
        :return: updated list
        """
        children = []
        for couple in csp_i.getNeighbour(root_i):  # check for every edges involving root
            if couple[0] == root_i:  # discards dual edges
                if couple[1] not in previous:  # if the other node is not in list, it is a child
                    children.append(couple[1])
        previous.append(root_i)  # adding the root to list...
        for var in children:
            _topSort(csp_i, var, previous)  # ... before to iterate for children
        return previous

    sequence = _topSort(csp, root, [])
    if len(sequence) == len(csp.getVariables()) and len(sequence) == len(set(sequence)):
        return sequence
    else:
        raise Exception  # It isn't a tree: EVERY var has to be ONE AND ONLY ONE time in the sequence


def treeSolver(csp: CSP) -> Assignment:
    """
    Finds a possible assignment for tree-like csp
    Execution time: O(nd^2) d=max cardinality
    :param csp:  csp of interest
    :return: an assignment, eventually null if the problem is unsatisfiable
    """
    def DAC(csp_i: CSP, sequence_i: List[Variable]) -> bool:
        """
        Directional Arc Consistency. Does inference over the domain, from the leaf to the root of the graph
        Execution time: O(nd^2) d=max cardinality
        :param csp_i: csp of interest
        :param sequence_i: topological order
        :return False if the csp is unsatisfiable, True otherwise
        """
        for i in range(len(sequence_i) - 1, -1, -1):
            for j in range(i-1, -1, -1):
                constraint = csp_i.findBinaryCostraint(sequence_i[j], sequence_i[i])
                if constraint is not None:
                    revise(sequence_i[j], constraint, sequence_i[i])
            if sequence_i[i].getActualDomainSize() == 0:
                return False
        return True

    assignment = Assignment()
    root = csp.getVariables().pop()
    sequence = topSort(csp, root)

    if not DAC(csp, sequence):      # is unsatisfiable
        nullAssignment = Assignment()
        nullAssignment.setNull()
        return nullAssignment

    for var in sequence:        # for each var in order...
        for value in var.getActualDomain():
            assignment.addVarAssigned(var, value)      # ... we try to assign a variable...
            if csp.assignmentConsistencyForVar(assignment, var):      # ... if the partial assignment is consistent...
                break           # ... we go to the next var
            else:
                assignment.removeVarAssigned(var)
        else:       # if none of the values is consistent, the csp is unsatisfiable and we return a null assignment
            nullAssignment = Assignment()
            nullAssignment.setNull()
            return nullAssignment

    return assignment
