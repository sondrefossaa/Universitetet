import sys

input = sys.stdin.readline


# check if any circles overlap from left to right
def read_line_as_int():
    return map(int, input().strip().split())


field = [200, 300]


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

    def __str__(self):
        return f"{self.comp}, {self.rank}"


# Dist squared is faster and avoids floation point presission issues
def dist_sq(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def check_overlap(c1, c2):
    cx1, cy1, r1 = c1
    cx2, cy2, r2 = c2
    return dist_sq((cx1, cy1), (cx2, cy2)) <= (r1 + r2) ** 2


k = int(input())

circles = []
uf = UnionFind(k + 2)
# Add virtual edges in union find for the edges of the field
L_EDGE = k
R_EDGE = k + 1
for i in range(k):
    circle = tuple(read_line_as_int())

    # If circkle overlaps edge, connect it to the virtual edge in union find
    # If it overlaps another circle, connect it to that circle in union find
    # If the left and right virtual edges are connected, then the field is blocked
    if circle[0] - circle[2] <= 0:  # Left overlap
        uf.union(i, L_EDGE)
    if circle[0] + circle[2] >= field[0]:  # Right overlap
        uf.union(i, R_EDGE)
    for j in range(i):
        if check_overlap(circle, circles[j]):
            uf.union(j, i)
    circles.append(circle)
    # print(uf.find(L_EDGE), uf.find(R_EDGE))
    # print(uf)
    if uf.find(L_EDGE) == uf.find(R_EDGE):
        print(i)
        exit()
print(0)
# print(uf)
