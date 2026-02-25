from sys import stdin
import heapq


def dijkstra(adj_rev, src, target):
    V = len(adj_rev)
    pq = []
    dist = [-1] * V
    dist[src] = s
    heapq.heappush(pq, (-dist[src], src))

    while pq:
        neg_d, u = heapq.heappop(pq)
        d = -neg_d

        if d < dist[u]:
            continue

        for v, t0, p, w in adj_rev[u]:
            max_dep = d - w

            if max_dep < t0:
                continue

            k = (max_dep - t0) // p
            dep_time = t0 + k * p

            if dep_time > dist[v]:
                dist[v] = dep_time
                heapq.heappush(pq, (-dist[v], v))

    return dist[target]


n, m, s = map(int, stdin.readline().split())

tramstops = []
for i in range(m):
    tramstops.append(tuple(map(int, stdin.readline().split())))

adj_rev = [[] for _ in range(n)]
for u, v, t0, p, d in tramstops:
    adj_rev[v].append((u, t0, p, d))

result = dijkstra(adj_rev, n - 1, 0)
print(result if result != -1 else "impossible")
