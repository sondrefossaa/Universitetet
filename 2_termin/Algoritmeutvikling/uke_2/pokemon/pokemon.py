# modulus
from sys import stdin
from collections import deque

kids, friendships, games = map(int, stdin.readline().split())
# each node of kid must be able to reach all other nodes

adj = [[] for _ in range(0, kids + 1)]
for line in stdin:
    kid1, kid2 = map(int, line.split())
    adj[kid1].append(kid2)
    adj[kid2].append(kid1)
print(adj)
seen = [False for _ in range(0, kids + 1)]
seen_count = 0
games_distribution = [0] * (kids + 1)
q = deque()

for kid in range(1, kids + 1):
    if seen[kid]:
        continue
    seen_count = 0
    current_game = 0
    q.append(kid)
    while q:
        curr = q.popleft()
        if seen[curr]:
            continue
        seen[curr] = True
        games_distribution[curr] = current_game % games + 1
        seen_count += 1
        current_game += 1
        for next in adj[curr]:
            q.append(next)

    if seen_count < games:
        print("impossible")
        exit()
print(" ".join(map(str, games_distribution[1:])), end="")
