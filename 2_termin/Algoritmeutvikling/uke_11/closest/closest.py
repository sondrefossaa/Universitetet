# Python program to find minimum distance between points

import math


# Function to compute Euclidean distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Function to find the minimum distance in the strip
def stripClosest(strip, d):
    min_dist = d
    p1 = p2 = None

    strip.sort(key=lambda point: point[1])

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) < min_dist:
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    p1, p2 = strip[i], strip[j]
            else:
                break

    return (min_dist, p1, p2)


# Divide and conquer function to find the minimum distance
def minDistUtil(points, left, right):

    # Base case brute force for 2 or fewer points
    if right - left <= 2:
        min_dist = float("inf")
        p1 = p2 = None

        for i in range(left, right):
            for j in range(i + 1, right):
                d = distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    p1, p2 = points[i], points[j]

        return (min_dist, p1, p2)

    # Find the midpoint
    mid = (left + right) // 2
    mid_x = points[mid][0]

    # Recursively find the minimum distances
    # in the left and right halves
    dl, l1, l2 = minDistUtil(points, left, mid)
    dr, r1, r2 = minDistUtil(points, mid, right)

    if dl < dr:
        d, p1, p2 = dl, l1, l2
    else:
        d, p1, p2 = dr, r1, r2
    # Build the strip of points within distance d from the midl
    strip = []
    for i in range(left, right):
        if abs(points[i][0] - mid_x) < d:
            strip.append(points[i])

    # Find the minimum distance in the strip
    stripDist, s1, s2 = stripClosest(strip, d)

    if stripDist < d:
        return (stripDist, s1, s2)
    else:
        return (d, p1, p2)

    return min(d, stripDist)


# Function to find the closest pair of points
def minDistance(points):
    points.sort(key=lambda point: point[0])
    return minDistUtil(points, 0, len(points))


while True:
    n = int(input())
    if n == 0:
        break

    points = []
    for _ in range(n):
        x, y = map(float, input().split())
        points.append((x, y))
    (
        dist,
        x,
        y,
    ) = minDistance(points)
    print(" ".join(map(str, x)), " ".join(map(str, y)))
