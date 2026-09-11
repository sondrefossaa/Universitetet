'''
    Implementation of a node in a search tree for the grid walk search problem
    Written by: Bjornar Tessem, Aug 2022
'''
from make_grid import legal_place, SIZE
import math

class GridWalkNode:
    '''
    A representation of a grid walk node within the grid search space as a pair of indices
    for example giving the position of a robot in the grid
    '''

    def __init__(self, i, j):
        '''
        Initializing a node i the search space
        :param i: row number
        :param j: column number
        '''
        self.i = i
        self.j = j

    @staticmethod
    def create_node(new_i, new_j):
        '''
        Creates a GridWalkNode if ok new place
        :param new_i: new row number
        :param new_j: new column number
        :return: a new node or None
        '''
        if legal_place(new_i, new_j):
            return GridWalkNode(new_i, new_j)
        else:
            return None

    def up_left(self):
        '''
        :return: GridWalkNode up left
        '''
        new_i = self.i-1
        new_j = self.j-1
        return self.create_node(new_i, new_j)

    def up(self):
        '''
        :return: GridWalkNode up
        '''
        new_i = self.i-1
        new_j = self.j
        return self.create_node(new_i, new_j)

    def up_right(self):
        '''
        :return: GridWalkNode up right
        '''
        new_i = self.i-1
        new_j = self.j+1
        return self.create_node(new_i, new_j)

    def left(self):
        '''
        :return: GridWalkNode left
        '''
        new_i = self.i
        new_j = self.j-1
        return self.create_node(new_i, new_j)

    def right(self):
        '''
        :return: GridWalkNode right
        '''
        new_i = self.i
        new_j = self.j+1
        return self.create_node(new_i, new_j)

    def down_left(self):
        '''
        :return: GridWalkNode down left
        '''
        new_i = self.i+1
        new_j = self.j-1
        return self.create_node(new_i, new_j)

    def down(self):
        '''
        :return: GridWalkNode down
        '''
        new_i = self.i+1
        new_j = self.j
        return self.create_node(new_i, new_j)

    def down_right(self):
        '''
        :return: GridWalkNode down right
        '''
        new_i = self.i + 1
        new_j = self.j + 1
        return self.create_node(new_i, new_j)

    def __eq__(self, other):
        '''
        checks if two GridWalkNodes are the same
        :param other: the node to check against
        :return: True if self and other board are identical in rows and columns
        '''
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        '''
        A hash function for the purpose of efficient set representation of GridWalkNodes
        Used in the search algorithms visited set
        :return: a hash function for self
        '''
        return self.i + self.j * 1000
