from sys import stdin, maxsize
import heapq


def wait_time(t0, d, p):
    return abs(t0 - d % p)


def dijkstra(s0, adj, src, target):
    V = len(adj)
    pq = []
    dist = [maxsize] * n
    dist[src] = s0
    # push a tuple of distance to source and the node
    heapq.heappush(pq, (s0, src))

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue
        if u == target:
            return d <= s
        for v, t0, p, d in adj[u]:
            # print(d, tramstops[u][3], w)
            # print("Old w: ", w)
            w = d + wait_time(t0, d, p)
            # print("New w: ", w)
            if dist[u] + w < dist[v] and dist[u] + w <= s:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))


n, m, s = map(int, stdin.readline().split())

tramstops = []

for i in range(m):
    # u, v, t0, p = map(int, stdin.readline().split())
    tramstops.append(tuple(map(int, stdin.readline().split())))

# Build adjacency
adj = [[] for _ in range(n)]
for u, v, t0, p, d in tramstops:
    adj[u].append((v, t0, p, d))
# print("Adjacent: ", adj)
# For each time the person can leave
# the larges found seconds after 0 he can leave
can_reach = -1
for i in range(s, -1, -1):
    if dijkstra(i, adj, 0, n - 1):
        can_reach = i
        break
print(can_reach if can_reach != -1 else "impossible")
# print(tramstops)


# From each second from 0 to s-1, check if you can reach the last tram stop before s seconds
# Shortest path algorithm, but reverse so longest?
# Start from end to start and relax weights reverse
# while len(sptSet) != m:
