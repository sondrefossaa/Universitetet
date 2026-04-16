import math
from collections import namedtuple
from sys import stdin

input = stdin.readline

Point = namedtuple("Point", "x y")
Sol = namedtuple("Sol", "delta pair")


def dist(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def bruteforce(points):
    best = Sol(float("inf"), (None, None))
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(points[i], points[j])
            if d < best.delta:
                best = Sol(d, (points[i], points[j]))
    return best


def compute_strip(strip, best):
    m = len(strip)
    ans = best
    for i in range(m):
        for j in range(i + 1, min(i + 8, m)):
            if strip[j].y - strip[i].y >= ans.delta:
                break
            d = dist(strip[i], strip[j])
            if d < ans.delta:
                ans = Sol(d, (strip[i], strip[j]))
    return ans


def closest(points):
    X = sorted(points, key=lambda p: (p.x, p.y))
    Y = sorted(points, key=lambda p: (p.y, p.x))
    return closest_pair(X, Y)


def closest_pair(X, Y):
    n = len(X)
    if n <= 3:
        return bruteforce(X)

    mid = n // 2
    midx = X[mid].x

    Xl = X[:mid]
    Xr = X[mid:]

    left_ids = {id(p) for p in Xl}
    Yl = []
    Yr = []
    for p in Y:
        if id(p) in left_ids:
            Yl.append(p)
        else:
            Yr.append(p)

    left_sol = closest_pair(Xl, Yl)
    right_sol = closest_pair(Xr, Yr)
    best = left_sol if left_sol.delta <= right_sol.delta else right_sol

    strip = [p for p in Y if abs(p.x - midx) < best.delta]
    return compute_strip(strip, best)


while True:
    n = int(input())
    if n == 0:
        break

    points = []
    for _ in range(n):
        x, y = map(float, input().split())
        points.append(Point(x, y))

    ans = closest(points)
    p1, p2 = ans.pair
    print(f"{p1.x} {p1.y} {p2.x} {p2.y}")
