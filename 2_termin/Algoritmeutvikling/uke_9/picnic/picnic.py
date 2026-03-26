from sys import stdin
from collections import namedtuple

input = stdin.readline

n = int(input())
Person = namedtuple("Person", ["pace", "superior"])
print(n)
people = {}
for _ in range(n):
    line = input().split()
    name = line[0]
    pace = float(line[1])
    superior = line[2]
    people[name] = Person(pace, superior)

print(people)


# Bottom up check if available if better choose.
# Post order
# def post_order(root=None):
#     if root:
#         post_order(root.left)
#         post_order(root.right)
#         print(root.val)

