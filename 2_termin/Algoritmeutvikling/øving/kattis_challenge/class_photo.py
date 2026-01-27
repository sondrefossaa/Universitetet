from sys import stdin
import math

lines = stdin.readlines()
print(math.prod(map(int, lines)))
