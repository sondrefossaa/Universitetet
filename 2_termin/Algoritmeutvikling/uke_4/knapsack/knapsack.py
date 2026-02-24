from sys import stdin


def solve(c, n, items):
    dp = [0] * (c + 1)
    keep = [[0] * (c + 1) for _ in range(n)]

    # For each item
    for i in range(n):
        val, w = items[i]
        for cap in range(c, w - 1, -1):
            new_value = dp[cap - w] + val
            if new_value > dp[cap]:
                dp[cap] = new_value
                keep[i][cap] = 1
    print(keep)
    print(dp)
    chosen = []
    max_val = max(dp)
    remaining_cap = dp.index(max_val)
    for i in range(n - 1, -1, -1):
        if remaining_cap <= 0:
            break
        if keep[i][remaining_cap]:
            chosen.append(i)
            remaining_cap -= items[i][1]
    chosen.reverse()

    print(len(chosen))
    if chosen:
        print(" ".join(map(str, chosen)))


while 1:
    try:
        c, n = map(int, stdin.readline().split())
        items = []
        for _ in range(n):
            v, w = map(int, stdin.readline().split())
            items.append((v, w))
        solve(c, n, items)
    except ValueError:
        break
