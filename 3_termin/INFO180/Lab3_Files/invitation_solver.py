'''
    This class solves a constraint satisfaction problem that involves logical constraints
    on who to invite to a party. It uses a depth-first strategy (with backtracking)
    Written by Bjornar Tessem, 31 Aug 2020
'''
from guest import Guest

from invitation_node import InvitationNode

class InvitationSolver:

    '''
        The class contains for a CSP solver that ims to find invitations of a set of potential guests to a party
        according to some constraints.
        The class contains the search strategy, which is basically a depth first search, but continued so it finds
        all solutions
    '''


    def __init__(self):
        '''
        Constructor that creates an empty search frontier for depth first search
        and then adds one node to the search tree that contains an empty assigmnent of guests
        self.count is just used for counting the nodes of the tree that is generated during search
        Notice the use of append() and pop() to realise a stack search frontier
        '''
        self.frontier = []
        self.frontier.append(InvitationNode())
        self.count = 1

    def run_search(self):
        '''
        runs a depth-first-search on the search tree.
        Notice: pop() in python removes the last element from a list
        :return: a solution of the search in the form of an InvitationNode
        '''
        while len(self.frontier) != 0:
            node = self.frontier.pop()
            if node.is_goal():
                return node
            self.update_frontier(node)
        return None

    def update_frontier(self, node):
        '''
        Finds new nodes to be added to the search frontier
        :param node: the node that we want to find children of
        :return: void
        '''
        new_nodes = node.get_neighbours()
        for node in new_nodes:
            self.count = self.count+1
            self.frontier.append(node)

if __name__ == "__main__":
    '''
        runs the invitation solver
    '''
    s = InvitationSolver()
    # initialize it
    sol = s.run_search()
    # run the first search
    count = 0
    while sol is not None:
        count = count+1
        print(sol)
        # print a solution
        sol = s.run_search()
        # find the next solution in the search tree

    print(count)
    # print the number of nodes investigated


