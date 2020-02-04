from timeit import default_timer as timer

from Cutset import *
from Map import *


def example1():     # Unsatisfiable
    csp = CSP()

    a = Variable('a', ['red', 'orange'])
    b = Variable('b', ['red', 'black'])
    c = Variable('c', ['red', 'black'])
    csp.addVariable(a)
    csp.addVariable(b)
    csp.addVariable(c)

    csp.addUnaryConstraint(a, Constraint(equals), 'orange')
    csp.addBinaryConstraint(b, Constraint(equals), a)
    csp.addBinaryConstraint(c, Constraint(equals), b)

    return csp


def example2():     # Tree
    csp = CSP()

    a = Variable('a', [1, 2, 3, 4])
    b = Variable('b', [1, 2, 3, 4])
    c = Variable('c', [1, 2, 3, 4])
    csp.addVariable(a)
    csp.addVariable(b)
    csp.addVariable(c)

    csp.addBinaryConstraint(a, Constraint(lesser), b)
    csp.addBinaryConstraint(b, Constraint(lesser), c)

    return csp


def example3():
    csp = CSP()

    a = Variable('a', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    b = Variable('b', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    csp.addVariable(a)
    csp.addVariable(b)

    def func(var1, var2):
        if var1 ** 2 == var2:
            return True
        else:
            return False

    csp.addBinaryConstraint(a, Constraint(func), b)

    return csp


def example4():     # Tree
    csp = CSP()

    x1 = Variable('x1', ['r', 'w', 'k'])
    x2 = Variable('x2', ['g', 'w', 'k'])
    x3 = Variable('x3', ['r', 'w', 'b'])
    x4 = Variable('x4', ['w', 'b', 'k'])
    csp.addVariable(x1)
    csp.addVariable(x2)
    csp.addVariable(x3)
    csp.addVariable(x4)

    csp.addBinaryConstraint(x1, Constraint(equals), x2)
    csp.addBinaryConstraint(x1, Constraint(equals), x3)
    csp.addBinaryConstraint(x3, Constraint(equals), x4)

    return csp


def example5():     # Tree
    csp = CSP()

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    a = Variable('a', values)
    b = Variable('b', values)
    c = Variable('c', values)
    d = Variable('d', values)
    e = Variable('e', values)
    f = Variable('f', values)
    g = Variable('g', values)
    h = Variable('h', values)
    i = Variable('i', values)
    csp.addVariable(a)
    csp.addVariable(b)
    csp.addVariable(c)
    csp.addVariable(d)
    csp.addVariable(e)
    csp.addVariable(f)
    csp.addVariable(g)
    csp.addVariable(h)
    csp.addVariable(i)

    csp.addBinaryConstraint(a, Constraint(lesser), b)

    csp.addBinaryConstraint(b, Constraint(lesser), g)
    csp.addBinaryConstraint(b, Constraint(lesser), d)
    csp.addBinaryConstraint(c, Constraint(lesser), e)
    csp.addBinaryConstraint(c, Constraint(lesser), f)
    csp.addBinaryConstraint(g, Constraint(lesser), h)
    csp.addBinaryConstraint(g, Constraint(lesser), i)
    csp.addBinaryConstraint(a, Constraint(lesser), c)
    return csp


def example6(n: int):     # almost a tree
    csp = CSP()

    values = [i for i in range(n)]

    for i in range(n):
        csp.addVariable(Variable(str(i), values))

    vars = list(csp.getVariables())
    var = vars[len(vars)-1]

    for i in range(len(vars)-2):
        csp.addBinaryConstraint(vars[i], Constraint(lesser), vars[i+1])
        csp.addBinaryConstraint(vars[i], Constraint(different), var)

    return csp


def australia():
    csp = CSP()

    values = ['red', 'green', 'blue']
    wa = Variable('wa', values)
    nt = Variable('nt', values)
    sa = Variable('sa', values)
    q = Variable('q', values)
    nsw = Variable('nsw', values)
    v = Variable('v', values)
    t = Variable('t', values)
    csp.addVariable(wa)
    csp.addVariable(nt)
    csp.addVariable(sa)
    csp.addVariable(q)
    csp.addVariable(nsw)
    csp.addVariable(v)
    csp.addVariable(t)

    csp.addBinaryConstraint(wa, Constraint(different), nt)
    csp.addBinaryConstraint(wa, Constraint(different), sa)
    csp.addBinaryConstraint(nt, Constraint(different), q)
    csp.addBinaryConstraint(nt, Constraint(different), sa)
    csp.addBinaryConstraint(sa, Constraint(different), q)
    csp.addBinaryConstraint(sa, Constraint(different), nsw)
    csp.addBinaryConstraint(sa, Constraint(different), v)
    csp.addBinaryConstraint(q, Constraint(different), nsw)
    csp.addBinaryConstraint(nsw, Constraint(different), v)

    return csp


def italy():
    csp = CSP()

    values = ['red', 'green', 'blue', 'yellow']
    va = Variable('Val d\'Aosta', values)
    pi = Variable('Piemonte', values)
    lo = Variable('Lombardia', values)
    tr = Variable('Trentino', values)
    ve = Variable('Veneto', values)
    f = Variable('Friuli', values)
    li = Variable('Liguria', values)
    er = Variable('Emilia', values)
    to = Variable('Toscana', values)
    um = Variable('Umbria', values)
    ma = Variable('Marche', values)
    la = Variable('Lazio', values)
    ab = Variable('Abruzzo', values)
    mo = Variable('Molise', values)
    cam = Variable('Campania', values)
    pu = Variable('Puglia', values)
    ba = Variable('Basilicata', values)
    cal = Variable('Calabria', values)
    si = Variable('Sicilia', values)
    sa = Variable('Sardegna', values)
    csp.addVariable(va)
    csp.addVariable(pi)
    csp.addVariable(lo)
    csp.addVariable(tr)
    csp.addVariable(ve)
    csp.addVariable(f)
    csp.addVariable(li)
    csp.addVariable(er)
    csp.addVariable(to)
    csp.addVariable(um)
    csp.addVariable(ma)
    csp.addVariable(la)
    csp.addVariable(ab)
    csp.addVariable(mo)
    csp.addVariable(cam)
    csp.addVariable(pu)
    csp.addVariable(ba)
    csp.addVariable(cal)
    csp.addVariable(si)
    csp.addVariable(sa)

    csp.addBinaryConstraint(va, Constraint(different), pi)
    csp.addBinaryConstraint(pi, Constraint(different), li)
    csp.addBinaryConstraint(pi, Constraint(different), lo)
    csp.addBinaryConstraint(pi, Constraint(different), er)
    csp.addBinaryConstraint(lo, Constraint(different), er)
    csp.addBinaryConstraint(lo, Constraint(different), tr)
    csp.addBinaryConstraint(lo, Constraint(different), ve)
    csp.addBinaryConstraint(tr, Constraint(different), ve)
    csp.addBinaryConstraint(f, Constraint(different), ve)
    csp.addBinaryConstraint(ve, Constraint(different), er)
    csp.addBinaryConstraint(li, Constraint(different), to)
    csp.addBinaryConstraint(li, Constraint(different), er)
    csp.addBinaryConstraint(er, Constraint(different), to)
    csp.addBinaryConstraint(er, Constraint(different), ma)
    csp.addBinaryConstraint(to, Constraint(different), um)
    csp.addBinaryConstraint(to, Constraint(different), la)
    csp.addBinaryConstraint(to, Constraint(different), ma)
    csp.addBinaryConstraint(um, Constraint(different), ma)
    csp.addBinaryConstraint(um, Constraint(different), la)
    csp.addBinaryConstraint(la, Constraint(different), ma)
    csp.addBinaryConstraint(la, Constraint(different), cam)
    csp.addBinaryConstraint(la, Constraint(different), ab)
    csp.addBinaryConstraint(la, Constraint(different), mo)
    csp.addBinaryConstraint(ma, Constraint(different), ab)
    csp.addBinaryConstraint(ab, Constraint(different), mo)
    csp.addBinaryConstraint(mo, Constraint(different), cam)
    csp.addBinaryConstraint(mo, Constraint(different), pu)
    csp.addBinaryConstraint(cam, Constraint(different), pu)
    csp.addBinaryConstraint(cam, Constraint(different), ba)
    csp.addBinaryConstraint(pu, Constraint(different), ba)
    csp.addBinaryConstraint(ba, Constraint(different), cal)

    return csp


def AC3_example(example: CSP):
    print("EXAMPLE: AC3")
    print('testing...')
    print('Certainly unsatisfiable: ' + str(not AC3(example)))
    example.printActualDomains()


def BT_example(example: CSP):
    print('EXAMPLE: Backtrack')
    print('testing...')
    backtrack(example).printAssignment()


def TS_example(example: CSP):
    print('EXAMPLE: TreeSolver')
    print('testing...')
    treeSolver(example).printAssignment()
