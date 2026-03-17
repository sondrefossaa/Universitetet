from sys import stdin
from collections import deque

# Run all bsf simulatious with same backward queue or cache the queue
input = stdin.readline
goal = "111110111100 110000100000"
max_depth = 10


def precompute_knight_moves():
    moves = [[] for _ in range(25)]
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
    return moves


knight_moves = precompute_knight_moves()

n = int(input())


class BidirectionalSearch:
    def __init__(self, start_state, goal_state) -> None:
        self.depth = 0
        self.fw = deque([start_state])
        self.bw = deque([goal_state])
        self.fw_visited = set()
        self.bw_visited = set()
        self.fw_move = 1
        self.bw_move = 0

    def get_moves(self, state):
        moves = []
        empty_idx = state.find(" ")

        for i in range(25):
            if state[i] != " ":
                if empty_idx in knight_moves[i]:
                    temp_state = list(state)
                    temp_knight = temp_state[i]
                    temp_state[i] = " "
                    temp_state[empty_idx] = temp_knight
                    moves.append("".join(temp_state))
        return moves

    def bsf(self, direction):
        if direction == "foreward":
            current_state = self.fw.popleft()
            for move in self.get_moves(current_state):
                if move not in self.fw_visited:
                    self.fw_visited.add(move)
                    self.fw.append(move)
        elif direction == "backward":
            current_state = self.bw.popleft()
            for move in self.get_moves(current_state):
                if move not in self.fw_visited:
                    self.bw_visited.add(move)
                    self.bw.append(move)

    def is_intersecting(self):
        return set(self.fw).intersection(set(self.bw))

    def bd_search(self):
        while self.fw and self.bw and self.depth < max_depth:
            self.depth += 1
            self.bsf(direction="foreward")
            self.bsf(direction="backward")

            if self.is_intersecting():
                return self.depth
                break
        return "Unsolvable in less than 11 move(s)."


for test_case in range(n):
    # Read all 5 lines and join them into a single string
    board_1d = "".join(input().strip() for _ in range(5))
    bd = BidirectionalSearch(board_1d, goal)
    print(bd.bd_search())

# print(list(board_1d))
# print(board_1d)
# print(knight_moves)
