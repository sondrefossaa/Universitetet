# Gale ryser
from sys import stdin

input = stdin.readline
m, n = map(int, input().split())
rows = list(map(int, input().split()))
cols = list(map(int, input().split()))

if sum(rows) != sum(cols):
    print("No")
    exit()

rows.sort(reverse=True)
cols.sort(reverse=True)

row_prefix = 0

for k in range(1, m + 1):
    row_prefix += rows[k - 1]

    col_capacity = 0
    for col in cols:
        if col < k:
            col_capacity += col
        else:
            col_capacity += k

    if row_prefix > col_capacity:
        print("No")
        break
else:
    print("Yes")
