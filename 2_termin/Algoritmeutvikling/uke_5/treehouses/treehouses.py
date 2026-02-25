# Minimum spanning tree?
# Union find?
# Find the nodes that need to be connected with union find and calculate the distances for all of them ez

from sys import stdin
from math import sqrt


class UnionFind:
    def __init__(self, size) -> None:
        self.comp = list(range(size))
        self.rank = [0] * size

    def find(self, u):
        if self.comp[u] == u:
            return u
        else:
            parent = self.find(self.comp[u])
            self.comp[u] = parent
            return parent

    def union(self, u, v):
        r1 = self.find(u)
        r2 = self.find(v)
        if self.rank[r1] < self.rank[r2]:
            self.comp[r1] = r2
        elif self.rank[r2] < self.rank[r1]:
            self.comp[r2] = r1
        else:
            self.comp[r1] = r2
            self.rank[r1] += 1

    def print(self):
        print(self.comp, self.rank)


# The first e of them in the list are close enough to neighboring open land around the rainforest so that transportation between all of them is easy by foot.
n, e, p = map(int, stdin.readline().split())

treehouses = []
uf = UnionFind(n)
for _ in range(n):
    treehouses.append(tuple(map(float, stdin.readline().split())))


for i in range(1, e):
    uf.union(0, i)


# Get connections

for i in range(p):
    x, y = map(int, stdin.readline().split())
    uf.union(x - 1, y - 1)

edges = []


def find_distance(t1, t2):
    x1, y1, x2, y2 = t1[0], t1[1], t2[0], t2[1]
    dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


for i in range(n):
    for j in range(i + 1, n):
        if uf.find(i) != uf.find(j):
            x1, y1 = treehouses[i]
            x2, y2 = treehouses[j]
            edges.append((i, j, find_distance(treehouses[i], treehouses[j])))

edges.sort(key=lambda x: x[2])

# Kruskal's algorithm

total_len = 0.0

for u, v, w in edges:
    if uf.find(u) != uf.find(v):
        uf.union(u, v)
        total_len += w

print(total_len)
