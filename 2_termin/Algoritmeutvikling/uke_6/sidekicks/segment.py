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
