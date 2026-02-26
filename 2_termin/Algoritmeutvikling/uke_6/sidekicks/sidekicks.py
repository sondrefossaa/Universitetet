from sys import stdin


class SegmentTree:
    def __init__(self, size):
        self.array = [0] * size
        self.n = size
        self.ST = [0] * (4 * self.n)

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

    def set_value(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)

    def sum(self, L, R):
        return self.query(1, 0, self.n - 1, L, R)


n, q = map(int, stdin.readline().split())

gemvalues = list(map(int, stdin.readline().strip().split()))
gemtypes = list(map(int, stdin.readline().strip()))
# print(gemtypes, gemvalues)

trees = [SegmentTree(n) for _ in range(6)]
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
