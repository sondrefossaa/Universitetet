from sys import stdin
from collections import deque

rows, cols = map(int, stdin.readline().split())
print(rows, cols)

currpos = list(map(int, stdin.readline().split()))
goalpos = list(map(int, stdin.readline().split()))

maze = []

i = 0
for line in stdin:
    maze.append(line.strip())
    i += 1
print(currpos, goalpos)


while (currpos != goalpos)
    #If Carl can turn left by 90 degrees and face an empty square, he will turn left 90 degrees and then move forward by one square.
    #Otherwise, if Carl can move forward by one square, he will do so.
    #Otherwise, he will turn right 90 degrees.
