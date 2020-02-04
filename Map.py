from __future__ import annotations
import random
from math import sqrt
import matplotlib.pyplot as plt
from CSP import *
from sys import setrecursionlimit


class Point:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def distance(self, target: Point) -> float:
        return sqrt((self._x - target.x())**2 + (self._y - target.y())**2)


class MapException:
    pass


class Map:
    def __init__(self, color: int = 4):
        self._region: Set[Point] = set()
        self._borders: Set[tuple] = set()
        colorList = ['red', 'blue', 'green', 'yellow']
        self._color: List = []
        for i in range(color):
            self._color.append(colorList[i])

    def addRegion(self, p: Point) -> None:
        if isinstance(p, Point):
            self._region.add(p)
        else:
            raise MapException

    def addBorder(self, p1: Point, p2: Point) -> None:
        if isinstance(p1, Point) and isinstance(p2, Point):
            self._borders.add((p1, p2))
        else:
            raise MapException

    def getRegions(self) -> Set[Point]:
        return self._region.copy()

    def getBorders(self) -> Set[tuple]:
        return self._borders.copy()

    def toCSP(self) -> CSP:
        """
        Transforms the map into a CSP
        :return: the CSP
        """
        csp = CSP()
        for p in self._region:
            v = Variable('region '+str('%.3f' % p.x())+'-'+str('%.3f' % p.y()), self._color)
            csp.addVariable(v)
        for l in self._borders:
            csp.addBinaryConstraint(csp.getVariable('region '+str('%.3f' % l[0].x())+'-'+str('%.3f' % l[0].y())), Constraint(different), csp.getVariable('region '+str('%.3f' % l[1].x())+'-'+str('%.3f' % l[1].y())))
        return csp

    def plot(self) -> None:
        """
        Plots the map
        """
        for l in self._borders:
            plt.plot([l[0].x(), l[1].x()], [l[0].y(), l[1].y()], 'k:')
        for p in self._region:
            plt.plot([p.x()], [p.y()], marker='o', markersize=5, color="black")
            plt.text(p.x()+.01, p.y()+.01, str('%.3f' % p.x())+'-'+str('%.3f' % p.y()), fontsize=7.5, color="red", weight="bold")
        plt.ylim(0, 1)
        plt.xlim(0, 1)
        plt.show()


def checkIntersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """
    Checks if segment AB intersect segment CD. It uses parametric equation of segments with 0.00005 precision
    :param a: start of segment AB
    :param b: end of segment AB
    :param c: start of segment CD
    :param d: end of segment CD
    :return: True if they intersect, False otherwise
    """
    tolerance = 0.00005

    def onSegment(a1: Point, b1: Point, p: Point) -> bool:
        """
        Checks if point P lies on the segment AB. It uses parametric equation of segments
        :param a1: start of segment AB
        :param b1: end of segment AB
        :param p: point P
        :return: True if P lies on AB, False otherwise
        """
        ax1 = a1.x()
        bx1 = b1.x()
        px1 = p.x()
        ay1 = a1.y()
        by1 = b1.y()
        py1 = p.y()

        if abs(bx1 - ax1) < tolerance:
            if abs(px1 - ax1) < tolerance:
                if min(ay1, by1) < py1 < max(ay1, by1):
                    return True
            return False
        if abs(by1 - ay1) < tolerance:
            if abs(py1 - ay1) < tolerance:
                if min(ax1, bx1) < px1 < max(ax1, bx1):
                    return True
            return False

        t1 = (px1 - ax1) / (bx1 - ax1)
        t2 = (py1 - ay1) / (by1 - ay1)
        if abs(t1 - t2) < tolerance:
            if 0 < t1 < 1:
                return True
        return False

    ax = a.x()
    bx = b.x()
    cx = c.x()
    dx = d.x()
    ay = a.y()
    by = b.y()
    cy = c.y()
    dy = d.y()

    det = ((ax - bx) * (dy - cy)) - ((dx - cx) * (ay - by))
    if abs(det) > tolerance:
        dt = ((dx - bx) * (dy - cy)) - ((dx - cx) * (dy - by))
        ds = ((ax - bx) * (dy - by)) - ((dx - bx) * (ay - by))
        t = round(dt/det, 5)
        s = round(ds/det, 5)
        if (0 < t < 1) and (0 < s < 1):
            return True
        else:
            return False
    else:
        if onSegment(a, b, c) or onSegment(a, b, d) or onSegment(c, d, a) or onSegment(c, d, b):
            return True
        return False


def linkPossible(links: Set[tuple], a: Point, b: Point) -> bool:
    """
    Checks if 2 points are linkable, given a set of links. In particular the link must not already be in links and don't intersect other links
    :param links: set of links
    :param a: start of link
    :param b: end of link
    :return: True if A and B are linkable, False otherwise
    """
    possible = True
    for link in links:
        if not (isinstance(link[0], Point) and isinstance(link[1], Point)):
            raise Exception
        inter = checkIntersect(link[0], link[1], a, b)
        if (a, b) in links or (b, a) in links or inter:
            if inter:
                checkIntersect(link[0], link[1], a, b)
            possible = False
            break
    return possible


def generateMap(n: int, *, numColor: int = 4, minimalCutsetSize: int = 1) -> Map:
    """
    Generate a map like explained in R&N 2010 exercise 6.10
    :param minimalCutsetSize: size of minimal cutset
    :param numColor: number of color for variables' domain in CSP
    :param n: number of region
    :return: generated map
    """
    def generatePoints(n_i: int) -> Set[Point]:
        """
        Generates n points in the unit square
        :param n_i: number of points
        :return: set of points
        """
        points_i = set()
        for i in range(0, n_i):
            points_i.add(Point(random.uniform(0, 1), random.uniform(0, 1)))
        return points_i

    def _dfs(root: Point, visited: Set[Point], links_i: Set[tuple], edges_i: Set[tuple]):
        visited.add(root)
        for link in links_i:
            if link[0] is root and link[1] not in visited:
                edges_i.add(link)
                _dfs(link[1], visited, links_i, edges_i)
            elif link[1] is root and link[0] not in visited:
                edges_i.add(link)
                _dfs(link[0], visited, links_i, edges_i)

    def _bfs(stack: List[Point], visited: Set[Point], links_i: Set[tuple], edges_i: Set[tuple]):
        while stack:
            root = stack.pop(0)
            visited.add(root)
            for link in links_i:
                if link[0] is root and link[1] not in visited and link[1] not in stack:
                    stack.append(link[1])
                    edges_i.add(link)
                elif link[1] is root and link[0] not in visited and link[0] not in stack:
                    stack.append(link[0])
                    edges_i.add(link)

    m = Map(numColor)

    points = generatePoints(n)
    for point in points:
        m.addRegion(point)

    links = set()
    while len(points) > 0:
        point = points.pop()
        orderedPoints = list(points)
        orderedPoints.sort(key=lambda p_i: p_i.distance(point))
        for p in orderedPoints:
            if linkPossible(links, point, p):
                links.add((point, p))
                points.add(point)
                break

    edges = set()
    setrecursionlimit(n*3)
    #_bfs([m.getRegions().pop()], set(), links, edges)
    _dfs(m.getRegions().pop(), set(), links, edges)
    for edge in edges:
        m.addBorder(edge[0], edge[1])

    # additionalEdges = 0
    # ps = m.getRegions()
    # cutset = set()
    # cutset.add(ps.pop())
    # while additionalEdges < 1:
    #     p1 = cutset.pop()
    #     p2 = ps.pop()
    #     if linkPossible(edges, p1, p2):
    #         m.addBorder(p1, p2)
    #         edges.add((p1, p2))
    #         cutset.add(p2)
    #         additionalEdges += 1
    #     else:
    #         ps.add(p2)
    #     cutset.add(p1)

    cutset = []
    ps = m.getRegions()
    for i in range(minimalCutsetSize):
        if len(cutset) == 0:
            cutset.append(ps.pop())
        else:
            p = cutset.pop()
            v = None
            for edge in edges:
                if edge[0] is p and edge[1] not in cutset:
                    v = edge[1]
                if edge[1] is p and edge[0] not in cutset:
                    v = edge[0]
            cutset.append(p)
            cutset.append(v)

        actual = cutset[len(cutset)-1]
        for reg in ps:
            if reg is not cutset:
                if linkPossible(edges, actual, reg):
                    m.addBorder(actual, reg)
                    edges.add((actual, reg))

    return m
