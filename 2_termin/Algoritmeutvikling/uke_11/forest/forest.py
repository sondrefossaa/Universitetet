# Graham scan
from sys import stdin

input = stdin.readline


def shoelace(hull):
    """Calculate area of convex hull using shoelace formula"""
    if len(hull) < 3:
        return 0.0

    area = 0
    n = len(hull)

    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]  # wrap to first point
        area += x1 * y2 - x2 * y1

    return abs(area) / 2.0


def leftturn(a, b, c):
    """Returns True if points a->b->c make a left turn (counter-clockwise)"""
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) > 0


def graham(points):
    points = sorted(set(points))
    S, hull = [], []  # S is a stack of points
    for p in points:
        while len(S) >= 2 and leftturn(S[-2], S[-1], p):
            S.pop()
        S.append(p)
    hull += S
    S = []
    for p in reversed(points):
        while len(S) >= 2 and leftturn(S[-2], S[-1], p):
            S.pop()
        S.append(p)
    hull += S[1:-1]
    return hull


p, a = map(int, input().split())

pines = [tuple(map(float, input().split())) for _ in range(p)]
aspens = [tuple(map(float, input().split())) for _ in range(a)]


p_hull = graham(pines)
a_hull = graham(aspens)
inter = polygon_intersection(p_hull, a_hull)
print(shoelace(inter))
