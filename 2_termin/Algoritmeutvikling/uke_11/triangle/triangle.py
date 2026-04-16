from sys import stdin

input = stdin.readline


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def d_area(x, y, z):
    return abs(cross(x, y, z))


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


n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]

hull = convex_hull(points)
m = len(hull)

if m < 3:
    print(0)
    exit()

best = 0

# Rotating calipers for maximum triangle area
# Go through all points in hull
for i in range(m):
    # k starts at the first possible thrid vertex after i
    k = i + 2
    # Try all later points as the second vertex
    for j in range(i + 1, m):
        if j == i:
            continue
        if k <= j:
            # Skip equal
            k = j + 1
        # No valid thrid vertex left
        if k >= m:
            break
        # Move k forward while the triangle area increases
        # For fixed i and j, the best k can be found by only moving forward since area goes up till a peak and then shrinks
        while k + 1 < m and d_area(hull[i], hull[j], hull[k + 1]) >= d_area(
            hull[i], hull[j], hull[k]
        ):
            k += 1

        best = max(best, d_area(hull[i], hull[j], hull[k]))

print(best / 2)
