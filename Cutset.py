from typing import Tuple

from Backtrack import *
from TreeSolver import *

import random


def randomVar(csp: CSP, assignment: Assignment) -> Variable:
    varAssignment: Dict[Variable] = assignment.getAssignment()
    unassigned = [var for var in list(csp.getVariables() - varAssignment.keys())]
    return unassigned[int(random.uniform(0, len(unassigned)-1))]


def isATree(csp: CSPWorkingCopy) -> bool:
    def _dfs(edges_i: Set[tuple], root_i: Variable, parent: Union[Variable, None], visited: Set[Variable]) -> bool:
        """
        DeptFirstSearch-like algorithm
        :param edges_i: all edges to visit
        :param root_i: variable from which it starts
        :param visited: already visited nodes
        :return: False if finds a cycle
        """
        neighbours = []
        del_edges = []
        for edge in edges_i:  # check for every edges involving root
            if edge[0] is root_i and not (edge[1] is parent):
                neighbours.append(edge[1])
                del_edges.append(edge)

        for edge in del_edges:
            edges_i.remove(edge)

        visited.add(root_i)  # adding the root to list...
        if len(set(neighbours) & visited) > 0:      # the graph is cyclic
            return False
        for neighbour in neighbours:
            if not _dfs(edges_i, neighbour, root_i, visited):  # ... before to iterate for children
                return False
        return True

    variables = csp.getVariables()
    edges = csp.getEdges()

    if len(variables) <= len(edges)/2:      # a tree have this property: #nodes = #edges + 1
        return False

    root = variables.pop()
    sequence = set()
    if _dfs(edges, root, None, sequence):
        if len(sequence) == len(csp.getVariables()):    # the graph isn't connected
            return True
    return False


def cutset(csp: CSP, *, heuristic=True) -> Tuple[Assignment, int]:
    """
    Given a csp, find a possible assignment
    :param csp: csp of interest
    :param heuristic: if True variables' order is chosen by MRV-HD, if False is chosen randomly
    :return: assignment that satisfies the csp, eventually null if it is unsatisfiable, and the size of remaining tree
    """

    def backtrackSearch(csp_i: CSP, problem_wc: CSPWorkingCopy, assignment_i: Assignment = None) -> Optional[Assignment]:
        """
        Executes backtracking search for a complete assignment of a csp
        :param problem_wc: it keep track of assigned var, so checking for tree is much more performing
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

        if isATree(problem_wc):
            subproblem = csp_i.subproblem(assignment_i)
            subAssignment = treeSolver(subproblem)

            nonlocal treeDimension
            treeDimension = len(subproblem.getVariables())
            if not subAssignment.isNull():
                return subAssignment + assignment_i
            else:
                return None

        if heuristic:
            var = orderVariables(csp_i, assignment_i)
        else:
            var = randomVar(csp_i, assignment_i)
        values = orderDomainValues(csp_i, assignment_i, var)

        for value in values:
            localAssignment = copy(assignment_i)            # we try to assign a var in a local copy of assignment
            localAssignment.addVarAssigned(var, value)
            if MAC(csp_i, localAssignment, csp_i.getNeighbour(var)):      # if it's possible to complete the assignment, we iterate...
                problem_wc.hideVar(var)
                result = backtrackSearch(csp_i, problem_wc, localAssignment)
                if result is not None:      # ... if it fails, we go back and propagate the None result
                    return result
                else:
                    problem_wc.unhideVar(var)
        return None

    treeDimension = 0
    assignment = backtrackSearch(csp, CSPWorkingCopy(csp))
    if assignment is None:
        nullAssignment = Assignment()
        nullAssignment.setNull()
        return nullAssignment, treeDimension
    return assignment, treeDimension
