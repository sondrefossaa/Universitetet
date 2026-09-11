from math import dist
from heuristic import Heuristic
from make_grid import SIZE

class PythagorasH(Heuristic):

    @staticmethod
    def h(node) -> float:
        goal_pos = (SIZE-1, SIZE-1)
        node_pos = (node.i, node.j)
        return dist(node_pos, goal_pos)
