# Edmonds–Karp algorithm
from collections import deque
from math import gcd


def create_path(parent, s, t):
    path = [t]
    while t != s:
        t = parent[t]
        path.append(t)
    return tuple(reversed(path))


def bfs(graph, s, t):
    q = deque([s])
    parent = {s: None}

    while q:
        v = q.popleft()
        for u in graph["E"][v]:
            if u in parent:
                continue  # Seen
            if graph["R"][v][u] <= 0:
                continue
            parent[u] = v
            q.append(u)
            if u == t:
                return create_path(parent, s, t)


def edges(p):
    return zip(p, p[1:])


def maxflow(graph, s, t):
    flow = 0
    while P := bfs(graph, s, t):
        b = min(graph["R"][v][u] for (v, u) in edges(P))
        flow += b
        for i in range(1, len(P)):
            v, u = P[i - 1], P[i]
            graph["R"][v][u] -= b
            graph["R"][u][v] += b
    return flow


n = int(input())
rooms = [int(input()) for _ in range(n)]

s = rooms.index(min(rooms))
t = rooms.index(max(rooms))

graph = {
    "V": list(range(n)),
    "E": [[] for _ in range(n)],
    "R": [[0] * n for _ in range(n)],
}

for i in range(n):
    for j in range(i + 1, n):
        # Check if there is a passage with gretest common denominator
        g = gcd(rooms[i], rooms[j])  # Greatest common denominator
        if g > 1:
            graph["R"][i][j] = g
            graph["R"][j][i] = g
            graph["E"][i].append(j)
            graph["E"][j].append(i)

print(maxflow(graph, s, t))
