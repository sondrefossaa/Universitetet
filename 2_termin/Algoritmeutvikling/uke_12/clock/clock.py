from sys import stdin

input = stdin.readline
FULL = 360000


def longest_prefix_suffix(pattern):
    n, k = 0, len(pattern)
    lps = [0] * k
    idx = 1
    while idx < k:
        if pattern[idx] == pattern[n]:
            n += 1
            lps[idx] = n
            idx += 1
        else:
            if n != 0:
                n = lps[n - 1]
            else:
                lps[idx] = 0
                idx += 1
    return lps


# KMP
def kmp(text, pattern, lps):
    n, k = len(text), len(pattern)
    txt_idx, pat_idx = 0, 0
    while txt_idx < n:
        if pattern[pat_idx] == text[txt_idx]:
            txt_idx += 1
            pat_idx += 1
            if pat_idx == k:
                yield txt_idx - k
                pat_idx = lps[pat_idx - 1]
        elif txt_idx < n and pattern[pat_idx] != text[txt_idx]:
            if pat_idx != 0:
                pat_idx = lps[pat_idx - 1]
            else:
                txt_idx += 1


n = int(input())
clock1 = sorted(list(map(int, input().split())))
clock2 = sorted(list(map(int, input().split())))

# Angle diff list + wrap around
gap1 = list(clock1[i + 1] - clock1[i] for i in range(n - 1))
gap1.append(360000 - clock1[-1] + clock1[0])
gap2 = list(clock2[i + 1] - clock2[i] for i in range(n - 1))
gap2.append(360000 - clock2[-1] + clock2[0])
gap2 = gap2 * 2
lps = longest_prefix_suffix(gap1)
found = any(kmp(gap2, gap1, lps))
print("possible" if found else "impossible")
