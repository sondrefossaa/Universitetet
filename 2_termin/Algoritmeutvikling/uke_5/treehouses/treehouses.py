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

# Get connections
for i in range(p):
    x, y = map(int, stdin.readline().split())
    uf.union(x, y)

cables = set()


def find_distance(t1, t2):
    x1, y1, x2, y2 = t1[0], t1[1], t2[0], t2[1]
    dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # print("DIstance", dist)
    return dist


# Dijkstra?


# for i in range(e, len(uf.comp)):
#     if uf.rank[i] == 0:
#         min_distance = float("inf")
#         closest = -1
#         for treehouse in treehouses:
#             if treehouse == treehouses[i]:
#                 continue
#             c_dist = find_distance(treehouse, treehouses[i])
#             if c_dist < min_distance:
#                 closest = treehouse
#                 min_distance = c_dist
#         uf.rank[treehouses.index(closest)] = 1
#         cables.add((treehouses[i], closest))
#
# connected = [[] for _ in range(max(uf.comp))]
#
# for i in range(max(uf.comp)):
#     for j in range(n):
#         if uf.comp[j] == i:
#             connected[i].append(j)
#
# print(connected)

# print(cables)
dist = 0
for cable in cables:
    dist += find_distance(cable[0], cable[1])
print(dist)
