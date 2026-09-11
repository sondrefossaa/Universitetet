'''
    Implementation of the search space for the grid walk search
    Written by: Bjornar Tessem, Aug 2022
'''

import time
from copy import deepcopy
from queue import Queue, LifoQueue, PriorityQueue

from grid_walk_node import GridWalkNode
from grid_walk_path import GridWalkPath
from make_grid import is_goal
from zero_h import ZeroH
from max_dim_h import MaxDimH
from pythagoras_h import PythagorasH
from approx_max_dim_h import ApproxMaxDimH
from heuristic import Heuristic



class GridWalkSpace:
    '''
    This class is a representation of the search space for grid walk search.
    It allows for various approaches to search for a solution
    '''

    HEURISTIC = Heuristic()

    @staticmethod
    def h(node):
                '''
                The heuristic used in the A/A* search
                :param node: the GridWalkNode to compute h-value for
                :return: the estimated distance to the goal
                '''

                return GridWalkSpace.HEURISTIC.h(node)

    def __init__(self, frontier = Queue(), heuristic = Heuristic()):
        '''
        Initialisation of the space
        '''
        self.start = GridWalkNode(0,0)
        # the search always starts in the upper left corner of the grid
        self.visited = set()
        # at start we have not visited any nodes (squares in the grid)

        # The search frontier is given in the argumentlist
        self.frontier = frontier
        GridWalkSpace.HEURISTIC = heuristic

        self.frontier.put(GridWalkPath([self.start],self.h(self.start)))
        # put the start node on the frontier
        # adding the start position's h-value as an estimate of length to goal state
        # the h-value is only useful in A search

    def solve(self):
        '''
        :return: path for grid walk solution
        '''
        start = time.time()
        # start time for timing

        while not self.frontier.empty():
            # if frontier is empty there is no solution
            next_path = self.frontier.get()
            # get the next path from the frontier
            last_node = next_path.node_list[-1]
            # get the last node of this path

            if is_goal(last_node.i, last_node.j):
                # if we have a solution

                end = time.time()
                # we stop timing
                print("Time: ", end-start)
                # print time spent

                print("Nodes visited ", len(self.visited)+1)
                # print the number of nodes visited in the search space

                print("Length: ", len(next_path.node_list), " Cost: ", next_path.cost)
                #print length and cost of path

                return next_path
                # and return the found path

            children = self.get_children(next_path)
            # else find the children for this path
            for child in children:
                # put children on the frontier
                self.frontier.put(child)

        print("No solution found")
        # print than no solutions are found

        return None


    def get_children(self, path):
        '''
        makes a list of paths that are children of the input path
        :param path: the path to add children for
        :return: the list of children paths
        '''
        children = []
        last = path.node_list[-1]
        # find the last node of the path

        if not self.is_visited(last):
            # only do this if the last one is not already visited
            # add moves by making moves where you move in
            # in different directions
            self.add_move(children, path.node_list, last.up_left())
            self.add_move(children, path.node_list, last.up())
            self.add_move(children, path.node_list, last.up_right())
            self.add_move(children, path.node_list, last.left())
            self.add_move(children, path.node_list, last.right())
            self.add_move(children, path.node_list, last.down_left())
            self.add_move(children, path.node_list, last.down())
            self.add_move(children, path.node_list, last.down_right())

            self.visited.add(last)
            # add last to the set of visited nodes

        return children

    def is_visited(self, last):
        '''
        checks if a node in the search space is already visited
        :param last: the node to check
        :return: true if already visitetd
        '''
        return last in self.visited

    def add_move(self, children, path, node):

        '''
        Adds a single new path to a set of paths contained in children
        Copies path and adds node into the copied path
        :param children: the set of paths to add the new path to
        :param path: the path to which a next move is added
        :param node: the new node in the search space that is added to the path
        :return: nothing
        '''
        if node is not None:

            new_path = deepcopy(path)
            # make a deep copy of path

            new_path.append(node)
            # append node to this path

            grid_path = GridWalkPath(new_path,self.h(node))
            # makes a new GridWalkPath object with the new path and the h value (for A search)

            children.append(grid_path)




if __name__ == '__main__':

    print("Breidde-først")
    sp = GridWalkSpace(Queue())
    sp.solve()
    print("Dybde-først")
    sp = GridWalkSpace(LifoQueue())
    sp.solve()
    print("Best-først")
    sp = GridWalkSpace(PriorityQueue())
    sp.solve()

    print("Best-først med max_dim")
    sp = GridWalkSpace(PriorityQueue(), MaxDimH())
    sp.solve()

    print("Best-først med euclidian distance")
    sp = GridWalkSpace(PriorityQueue(), PythagorasH())
    sp.solve()

    print("Best-først med approx max dim")
    sp = GridWalkSpace(PriorityQueue(), ApproxMaxDimH())
    sp.solve()
