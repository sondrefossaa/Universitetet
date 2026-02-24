from collections import deque
from sys import stdin

n, m, c = map(int, stdin.readline().split())

sample = list(map(int, stdin.readline().split()))

ans = []


def slidemin(data, m):
    minq = deque()  # from collections
    maxq = deque()
    for i in range(len(data)):
        if minq and minq[0] == i - m:
            minq.popleft()
        while minq and data[minq[-1]] >= data[i]:
            minq.pop()
        minq.append(i)
        # Max
        if maxq and maxq[0] == i - m:
            maxq.popleft()
        while maxq and data[maxq[-1]] <= data[i]:
            maxq.pop()
        maxq.append(i)
        if i >= m - 1:
            if sample[maxq[0]] - sample[minq[0]] <= c:
                ans.append(str(i - m + 2))


slidemin(sample, m)

if ans:
    print("\n".join(ans))
else:
    print("NONE")
