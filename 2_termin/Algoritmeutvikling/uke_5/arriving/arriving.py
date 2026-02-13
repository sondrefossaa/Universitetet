from sys import stdin, maxsize
import heapq


def dijkstra(adj, src):
    V = len(adj)
    pq = []
    dist = [maxsize] * V
    dist[src] = 0
    # push a tuple of distance to source and the node
    heapq.heappush(pq, (0, src))

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist


sptSet = set()
n, m, s = map(int, stdin.readline().split())

tramstops = []

for i in range(m):
    # u, v, t0, p = map(int, stdin.readline().split())
    tramstops.append(tuple(map(int, stdin.readline().split())))

# Build adjacency
adj = [[] for _ in range(m)]
for i in range(m):
    for j in range(m):
        if tramstops[i][0] == tramstops[j][1]:
            adj[i].append((j, tramstops[j][4]))


print(tramstops)


# From each second from 0 to s-1, check if you can reach the last tram stop before s seconds
# Shortest path algorithm, but reverse so longest?
# Start from end to start and relax weights reverse
# while len(sptSet) != m:
