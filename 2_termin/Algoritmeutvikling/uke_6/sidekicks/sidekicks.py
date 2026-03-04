from sys import stdin


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


n, q = map(int, stdin.readline().split())

gemvalues = list(map(int, stdin.readline().strip().split()))
gemtypes = list(map(int, stdin.readline().strip()))
# print(gemtypes, gemvalues)

trees = [FenwickTree(n) for _ in range(6)]
gem_pos = [[] for _ in range(6)]
for i in range(n):
    gem_pos[gemtypes[i] - 1].append(i)
    trees[gemtypes[i] - 1].set_value(i, 1)

for i in range(q):
    a, b, c = map(int, stdin.readline().strip().split())
    match a:
        case 1:
            old_type = gemtypes[b - 1]
            gemtypes[b - 1] = c
            trees[old_type - 1].set_value(b - 1, 0)
            trees[c - 1].set_value(b - 1, 1)
        case 2:
            gemvalues[b - 1] = c
        case 3:
            total = 0
            for i in range(6):
                total += trees[i].sum(b - 1, c - 1) * gemvalues[i]
            print(total)
