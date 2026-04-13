import sys
from math import sqrt
from itertools import permutations


input_data = sys.stdin.read().split("\n")
idx = 0

n = int(input_data[idx])
idx += 1
locations = {}
for _ in range(n):
    parts = input_data[idx].split()
    idx += 1
    locations[parts[0]] = (float(parts[1]), float(parts[2]))


def dist(a, b):
    ax, ay = locations[a]
    bx, by = locations[b]
    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def path_len(stops):
    nodes = ["work"] + list(stops) + ["home"]
    return sum(dist(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1))


while idx < len(input_data):
    line = input_data[idx].strip()
    idx += 1
    if not line:
        continue
    stops = line.split()
    best = min(permutations(stops), key=path_len)
    print(" ".join(best))
