from sys import stdin

input = stdin.readline


def get_value(c):
    if c.isdigit():
        return int(c)
    elif c.islower():
        return ord(c) - ord("a") + 10
    else:
        return ord(c) - ord("A") + 36


def smaller_base62(a, b):
    # Can only be eq if same len
    if len(a) != len(b):
        return len(a) < len(b)
    # Compare values left to right
    for x, y in zip(a, b):
        if get_value(x) != get_value(y):
            return get_value(x) < get_value(y)
    # Equal
    return False


n = int(input())

for _ in range(n):
    s1 = input().strip()
    s2 = input().strip()

    if (s1 < s2) == (smaller_base62(s1, s2)):
        print("YES")
    else:
        print("NO")
