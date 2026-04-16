from sys import stdin

input = stdin.readline

L = int(input())
large = [tuple(map(int, input().split())) for _ in range(L)]
S = int(input())
small = [tuple(map(int, input().split())) for _ in range(S)]


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


# Graham scan
def convex_hull(points):
    points = sorted(set(points))
    S, hull = [], []  # S is a stack of points
    for p in points:
        while len(S) >= 2 and cross(S[-2], S[-1], p) <= 0:
            S.pop()
        S.append(p)
    hull += S
    S = []
    for p in reversed(points):
        while len(S) >= 2 and cross(S[-2], S[-1], p) <= 0:
            S.pop()
        S.append(p)
    hull += S[1:-1]  # ignore endpoints
    return hull


hull = convex_hull(large)


# Bin search to determine if point in polygon
def point_in_convex_polygon(p):
    n = len(hull)
    lo, hi = 1, n - 1
    if cross(hull[0], hull[1], p) < 0:
        return False
    if cross(hull[0], hull[-1], p) > 0:
        return False
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cross(hull[0], hull[mid], p) >= 0:
            lo = mid
        else:
            hi = mid

    # Check if p is inside triangle (hull[0], hull[lo], hull[lo+1])
    return cross(hull[lo], hull[(lo + 1) % n], p) >= 0


print(sum(point_in_convex_polygon(p) for p in small))
