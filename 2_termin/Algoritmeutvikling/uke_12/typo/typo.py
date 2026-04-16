# TOO SLOW
# Use hash of left right karp algo, something like that
from sys import stdin

input = stdin.readline


def trie(words):
    root = {}
    for word in words:
        current = root
        for letter in word:
            current = current.setdefault(letter, {})
        current["*"] = "*"
    return root


def find(t, w):
    current = t
    for letter in w:
        if letter not in current:
            return None  # Not found
        current = current[letter]
    return "*" in current  # Returns if node in tree


n = int(input())
dict = [input().strip() for _ in range(n)]

T = trie(dict)
ans = []
for word in dict:
    wl = len(word)
    for i in range(wl):
        if find(T, word[:i] + word[i + 1 :]):
            ans.append(word)
            break
print("\n".join(ans) if ans else "NO TYPOS")
