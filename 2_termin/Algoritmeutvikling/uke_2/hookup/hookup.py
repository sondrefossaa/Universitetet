# find a node that can be reached from two different start nodes

from collections import deque
from sys import stdin


stations, connections = map(int, stdin.readline().split())
adj = [[] for _ in range(stations + 1)]

for _ in range(connections):
    to_station, from_station = map(int, stdin.readline().split())
    adj[to_station].append(from_station)

# print(adj)
mystart, huzzstart = map(int, stdin.readline().split())


def get_reach(start):
    seen = [False for _ in range(stations + 1)]
    reach = set([start])
    q = deque()
    q.append(start)
    while q:
        curr = q.popleft()
        if seen[curr]:
            continue
        seen[curr] = True
        for next in adj[curr]:
            reach.add(next)
            q.append(next)
    return reach


myreach, huzzreach = get_reach(mystart), get_reach(huzzstart)
result = myreach.intersection(huzzreach)
if result:
    print("yes")
    print(list(result)[0])
else:
    print("no")
