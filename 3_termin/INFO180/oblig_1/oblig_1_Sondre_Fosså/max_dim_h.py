from heuristic import Heuristic
from make_grid import SIZE


class MaxDimH(Heuristic):

    @staticmethod
    def h(node):
        target_i = SIZE -1
        target_j = SIZE -1

        row_diff = abs(target_i - node.i)
        col_diff = abs(target_j - node.j)

        return max(row_diff, col_diff)
