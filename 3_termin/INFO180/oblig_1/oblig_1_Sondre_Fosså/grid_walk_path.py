'''
    Class representing a path in a search space and its cost
    Written by Bjornar Tessem, August 2022
'''
from make_grid import THE_GRID, THE_COST


class GridWalkPath:
    '''
    The representation of a search path
    '''

    def __init__(self, the_path=[], the_h=0):
        '''
        Cosntructor for GridWalkPath
        :param the_path: the path as a list of GridWalk Nodes
        :param the_h: the h-value for the last node in the path
        '''
        self.node_list = the_path
        self.cost = 0
        for node in self.node_list:
            # compute the cost of the path so far
            self.cost = self.cost + THE_COST[node.i][node.j]
        self.h = the_h

    def __lt__(self, other):
        '''
        Computes the total heuristic f for the AStarPath based on the length so far +
        the h-value. Used for ranking the paths in the  PriorityQueue of the GridWalkSpace solve
        :param other: the one to compare with self
        :return: True if the total heuristic f for self is smaller than for other
        '''
        self_f = self.cost + self.h
        other_f = other.cost + other.h
        return self_f < other_f
