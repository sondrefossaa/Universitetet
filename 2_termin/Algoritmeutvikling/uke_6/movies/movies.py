from sys import stdin


class SegmentTree:
    def __init__(self, array):
        self.n = len(array)
        self.ST = [0] * (2 * self.n)
        for i, v in enumerate(array):
            self.ST[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.ST[i] = self.ST[2 * i] + self.ST[2 * i + 1]

    def set_value(self, idx, val):
        idx += self.n
        self.ST[idx] = val
        idx >>= 1
        while idx:
            self.ST[idx] = self.ST[2 * idx] + self.ST[2 * idx + 1]
            idx >>= 1

    def sum(self, l, r):
        res = 0
        l += self.n
        r += self.n + 1
        while l < r:
            if l & 1:
                res += self.ST[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.ST[r]
            l >>= 1
            r >>= 1
        return res


cases = int(stdin.readline())
for _ in range(cases):
    movies, req = map(int, stdin.readline().split())
    last_idx = movies
    # Movie 1 at top
    movie_pos = [movies - 1 - i for i in range(movies)]

    arr = [0] * (movies + req)
    for i in range(movies):
        arr[i] = 1
    ST = SegmentTree(arr)
    for movie in map(int, stdin.readline().split()):
        pos = movie_pos[movie - 1]
        above = ST.sum(pos + 1, last_idx - 1)
        print(above, end=" ")
        ST.set_value(pos, 0)
        movie_pos[movie - 1] = last_idx
        ST.set_value(last_idx, 1)
        last_idx += 1
    print()
