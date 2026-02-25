from sys import stdin, maxsize
import heapq


# Work backwards from goal to get the latest time you can go


def wait_time(t0, d, p):
    if d < t0:
        return maxsize
    if p == 0:
        return d - t0
    return (p - ((d - t0) % p)) % p


def dijkstra(adj_rev, src, target):
    V = len(adj_rev)
    pq = []
    dist = [-1] * V
    dist[target] = s
    # push a tuple of distance to source and the node
    heapq.heappush(pq, (-dist[target], target))

    while pq:
        neg_d, u = heapq.heappop(pq)
        d = -neg_d
        if d < -dist[u]:
            continue
        # if u == src:
        #     return d <= s
        for v, t0, p, d in adj_rev[u]:
            new_d = d + wait_time(t0, d, p)
            if new_d > dist[v]:
                dist[v] = new_d
                heapq.heappush(pq, (-dist[v], v))
    return dist[0]


n, m, s = map(int, stdin.readline().split())

tramstops = []

for i in range(m):
    tramstops.append(tuple(map(int, stdin.readline().split())))
print(tramstops)
# Build adj_revacency
adj_rev = [[] for _ in range(n)]
for u, v, t0, p, d in tramstops:
    adj_rev[v].append((u, t0, p, d))

# print("Adj reversed: ", adj_rev)
# For each time the person can leave
# the larges found seconds after 0 he can leave
can_reach = dijkstra(adj_rev, 0, n - 1)
print(can_reach if can_reach != -1 else "impossible")

# print(tramstops)


# From each second from 0 to s-1, check if you can reach the last tram stop before s seconds
# Shortest path algorithm, but reverse so longest?
# Start from end to start and relax weights reverse
# while len(sptSet) != m:
