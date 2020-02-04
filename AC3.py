from CSP import *


def revise(varI: Variable, constraint: Constraint, varJ: Variable) -> bool:
    """
    Check for every value in the first variable's domain if exist a value of neighbour's domain compatible with it;
    if it doesn't exist, the value will be hidden
    Execution time: O(d^2) d=max cardinality
    :param varI: first variable
    :param constraint: constraint between the variables
    :param varJ: second variable
    :return: True if the domain has been reduced, False otherwise
    """
    revised = False
    for valueX in varI.getActualDomain():
        for valueY in varJ.getActualDomain():
            if constraint(valueX, valueY):
                break
        else:
            varI.hideValue(valueX)
            revised = True
    return revised


def AC3(csp: CSP) -> bool:
    """
    Reduce CSP's variable's domain by inference, maintaining arc consistency
    Execution time: O(nd^3) d=max cardinality
    :param csp: CSP
    :return: False if the CSP is unsatisfiable
    """
    def unaryRevise(var_i: Variable, constraint_i: Constraint, value_i: Any) -> None:
        """
        Check for every value of the variable if it is compatible with a unary constraint involving this variable;
        if it doesn't, the value will be hidden
        :param var_i: variable
        :param constraint_i: constraint
        :param value_i: value
        :return: None
        """
        for valueX in var_i.getActualDomain():
            if not constraint_i(valueX, value_i):
                var_i.hideValue(valueX)

    # Inference over the unary constraint
    for var in csp.getUnaryConstraints():
        for value in csp.getUnaryConstraintsForVar(var):
            unaryRevise(var, csp.findUnaryConstraint(var, value), value)

    # Inference over the binary constraints
    s = csp.getEdges()
    while len(s) is not 0:
        edge = s.pop()      # Take an edge...
        constraint = csp.findBinaryCostraint(edge[0], edge[1])
        varI = edge[0]
        varJ = edge[1]
        if revise(varI, constraint, varJ):      # ... and analise the relative constraint. If has been made inference, we have to check something
            if varI.getActualDomainSize() == 0:     # If a domain is empty, the csp is unsatisfiable
                return False
            otherConstraints = csp.getBinaryConstraintsForVar(varI)     # get others constraints involving inferenced variable...
            otherEdges = set()
            for var in otherConstraints:
                if var != varJ:
                    otherEdges.add((var, varI))         # ... convert them to edges ...
            s = s.union(otherEdges)         # ... and add them to the set of edges to analise
    return True
