from heuristic import Heuristic


class ZeroH(Heuristic):

    @staticmethod
    def h(node):
        return 0