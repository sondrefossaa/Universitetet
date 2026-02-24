from sys import stdin, maxsize
import heapq


def dijkstra(adj_rev, src, target):
    V = len(adj_rev)
    pq = []
    dist = [-1] * V
    dist[src] = s
    # push a tuple of distance to source and the node
    heapq.heappush(pq, (-dist[src], src))

    while pq:
        neg_d, u = heapq.heappop(pq)
        d = -neg_d
        if d > dist[u]:
            continue

        for v, t0, p, w in adj_rev[u]:
            if d - w > t0:
                continue
            a = d - w
            b = a % p
            dist[v] = a - b
            heapq.heappush(pq, (-dist[v], v))

    return dist[target]


n, m, s = map(int, stdin.readline().split())

tramstops = []

for i in range(m):
    tramstops.append(tuple(map(int, stdin.readline().split())))
print(tramstops)

# Build adj_rev
adj_rev = [[] for _ in range(n)]
for u, v, t0, p, d in tramstops:
    adj_rev[v].append((u, t0, p, d))

can_reach = dijkstra(adj_rev, n - 1, 0)
print(can_reach if can_reach != -1 else "impossible")
