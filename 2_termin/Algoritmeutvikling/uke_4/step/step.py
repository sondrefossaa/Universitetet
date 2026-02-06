from collections import deque
from sys import stdin

sx, sy, ex, ey, m1x, m1y, m2x, m2y = map(int, stdin.read().split())

ex -= sx
ey -= sy
m1x -= sx
m1y -= sy
m2x -= sx
m2y -= sy
sx = sy = 0

cells = [[0] * (ex + 1) for _ in range(ey + 1)]

cells[m1y][m1x] = -1
cells[m2y][m2x] = -1

# Mark destination
cells[ey][ex] = 1

q = deque([(ex, ey)])

while q:
    x, y = q.popleft()

    # Skip mine
    if cells[y][x] == -1:
        continue

    if x - 1 >= 0 and cells[y][x - 1] != -1:
        cells[y][x - 1] += cells[y][x]
        if (x - 1, y) not in q:
            q.append((x - 1, y))

    if y - 1 >= 0 and cells[y - 1][x] != -1:
        cells[y - 1][x] += cells[y][x]
        if (x, y - 1) not in q:
            q.append((x, y - 1))

print(cells[0][0])
