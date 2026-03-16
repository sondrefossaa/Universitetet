from sys import stdin

input = stdin.readline

n = int(input())

for i in range(n):
    matrix = []

    for i in range(5):
        matrix.append(input().strip())
    print(matrix)

    # Position mapping: (row, col) -> index = row*5 + col
    def precompute_knight_moves():
        moves = [[] for _ in range(25)]
        # All possible knight move offsets
        knight_offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for r in range(5):
            for c in range(5):
                pos = r * 5 + c
                for dr, dc in knight_offsets:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 5 and 0 <= nc < 5:
                        moves[pos].append(nr * 5 + nc)
        return moves  # moves[position] = list of reachable positions
