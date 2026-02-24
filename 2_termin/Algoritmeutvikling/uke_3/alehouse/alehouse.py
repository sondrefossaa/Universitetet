from sys import stdin

n, k = map(int, stdin.readline().split())
points = []

for _ in range(n):
    a, b = map(int, stdin.readline().split())
    points.append((a - k, 1))
    points.append((b, -1))

points.sort(key=lambda x: (x[0], -x[1]))

max_friends = 0
current = 0
for _, delta in points:
    current += delta
    max_friends = max(max_friends, current)

print(max_friends)
