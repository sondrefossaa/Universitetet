import sys


def input():
    return sys.stdin.readline().strip()


def ints():
    return map(int, sys.stdin.readline().split())


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


class SegmentTree:
    def __init__(self, size):
        self.array = [0] * size
        self.n = size
        self.ST = [0] * (4 * self.n)

    def build(self, node, L, R):
        if L == R:
            self.ST[node] = self.array[L]
        else:
            # Find mid
            mid = (L + R) // 2

            # Left half
            self.build(2 * node, L, mid)
            # Right half
            self.build(2 * node + 1, mid + 1, R)

            # Store sum of children in node
            self.ST[node] = self.ST[2 * node] + self.ST[2 * node + 1]

    def update(self, node, L, R, idx, val):
        if L == R:
            self.array[idx] = val
            self.ST[node] = val
        else:
            mid = (L + R) // 2

            if L <= idx <= mid:
                self.update(2 * node, L, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, R, idx, val)

            self.ST[node] = self.ST[2 * node] + self.ST[2 * node + 1]

    def query(self, node, tl, tr, l, r):
        if r < tl or tr < l:
            return 0

        if l <= tl and tr <= r:
            return self.ST[node]
        tm = (tl + tr) // 2

        return self.query(2 * node, tl, tm, l, r) + self.query(
            2 * node + 1, tm + 1, tr, l, r
        )

    def add_value(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)

    def sum(self, L, R):
        return self.query(1, 0, self.n - 1, L, R)


class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.array = [0] * size
        self.bit = [0] * (size + 1)  # 1-indexed Fenwick tree

    def _update(self, idx, delta):
        i = idx + 1  # Convert to 1-indexed
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def _query(self, idx):
        res = 0
        i = idx + 1  # Convert to 1-indexed
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

    def set_value(self, idx, val):
        delta = val - self.array[idx]
        self.array[idx] = val
        self._update(idx, delta)

    def sum(self, L, R):
        if L == 0:
            return self._query(R)
        return self._query(R) - self._query(L - 1)
