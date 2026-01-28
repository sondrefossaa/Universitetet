from sys import stdin

n, seconds = map(int, stdin.readline().split())
enters = []
exits = []
for _ in range(n):
    enter, exit = map(int, stdin.readline().split())
    enters.append(enter)
    exits.append(exit)
met = 0
curr_met = 0

for i in range(max(exits)):
    curr_met = 0
    for j in range(n):
        if exits[j] >= i + seconds - enters[j] <= i:
            curr_met += 1
    met = max(curr_met, met)
print(met)
