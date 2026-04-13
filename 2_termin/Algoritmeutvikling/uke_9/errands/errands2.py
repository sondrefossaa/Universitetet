import sys
from math import hypot

data = sys.stdin.read().strip().splitlines()
idx = 0

n = int(data[idx])
idx += 1

locations = {}
for _ in range(n):
    name, x, y = data[idx].split()
    idx += 1
    locations[name] = (float(x), float(y))


def dist(a, b):
    ax, ay = locations[a]
    bx, by = locations[b]
    return hypot(ax - bx, ay - by)


# Held-Karp
def solve_day(stops):
    m = len(stops)
    if m == 0:
        return []
    if m == 1:
        return stops

    INF = float("inf")

    # DP[mask][v] = minimum cost to start at work,
    # visit exactly the stops in mask, and end at stop v
    DP = [[INF] * m for _ in range(1 << m)]
    parent = [[-1] * m for _ in range(1 << m)]

    # base case
    for v in range(m):
        DP[1 << v][v] = dist("work", stops[v])

    # recurrence
    for mask in range(1 << m):
        for v in range(m):
            if not (mask & (1 << v)):
                continue
            if mask == (1 << v):
                continue

            prev_mask = mask ^ (1 << v)
            for u in range(m):
                if not (prev_mask & (1 << u)):
                    continue
                new_cost = DP[prev_mask][u] + dist(stops[u], stops[v])
                if new_cost < DP[mask][v]:
                    DP[mask][v] = new_cost
                    parent[mask][v] = u

    # Bitmask trick to make 111 m -1 times
    full_mask = (1 << m) - 1

    # finish at home
    best_cost = INF
    last = -1
    for v in range(m):
        total = DP[full_mask][v] + dist(stops[v], "home")
        if total < best_cost:
            best_cost = total
            last = v

    # reconstruct answer
    order = []
    mask = full_mask
    cur = last
    while cur != -1:
        order.append(stops[cur])
        next = parent[mask][cur]
        mask ^= 1 << cur
        cur = next

    order.reverse()
    return order


while idx < len(data):
    line = data[idx].strip()
    idx += 1
    if not line:
        continue
    stops = line.split()
    print(" ".join(solve_day(stops)))
