from sys import stdin
from collections import deque

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
        self.fw_visited = {start_state: 0}
        self.bw_visited = {goal_state: 0}

    def get_moves(self, state):
        moves = []
        empty_idx = state.find(" ")

        for i in range(25):
            if state[i] != " " and empty_idx in knight_moves[i]:
                temp_state = list(state)
                temp_state[i], temp_state[empty_idx] = " ", temp_state[i]
                moves.append("".join(temp_state))
        return moves

    def bsf(self, direction):
        if direction == "forward":
            level_size = len(self.fw)
            for _ in range(level_size):
                current_state = self.fw.popleft()
                for move in self.get_moves(current_state):
                    if move in self.bw_visited:
                        return (
                            self.fw_visited[current_state] + 1 + self.bw_visited[move]
                        )
                    if move not in self.fw_visited:
                        self.fw_visited[move] = self.fw_visited[current_state] + 1
                        self.fw.append(move)
        elif direction == "backward":
            level_size = len(self.bw)
            for _ in range(level_size):
                current_state = self.bw.popleft()
                for move in self.get_moves(current_state):
                    if move in self.fw_visited:
                        return (
                            self.fw_visited[move] + 1 + self.bw_visited[current_state]
                        )
                    if move not in self.bw_visited:
                        self.bw_visited[move] = self.bw_visited[current_state] + 1
                        self.bw.append(move)
        return None

    def bd_search(self):
        # Check if goal and start state is the same
        if self.fw_visited.keys() & self.bw_visited.keys():
            return "Solvable in 0 move(s)."
        while self.fw and self.bw and self.depth < max_depth:
            self.depth += 1

            result = self.bsf("forward")
            if result is not None and result <= max_depth:
                return f"Solvable in {result} move(s)."

            result = self.bsf("backward")
            if result is not None and result <= max_depth:
                return f"Solvable in {result} move(s)."

        return "Unsolvable in less than 11 move(s)."


for test_case in range(n):
    # Problem with removremoving traveling space charactering traveling space character
    board_lines = []
    for _ in range(5):
        line = input().rstrip("\n")
        board_lines.append(line)

    board_1d = "".join(board_lines)

    bd = BidirectionalSearch(board_1d, goal)
    print(bd.bd_search())

