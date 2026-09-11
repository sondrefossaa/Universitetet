'''
    Code that creates a random grid for the grid walk problem
    Programmed by Bjørnar Tessem, August 2022
'''

import random

SIZE = 100

def make_random_grid(size = 100,prob = 0.35, seed = 5001):
    '''
    Makes the random grid and the costs for each place in a square grid
    :param size: the size of the grid side
    :param prob: the probability of a square being unaccessible
    :param seed: a number used to initialize the random number generator
    :return: a final grid
    '''
    global SIZE
    SIZE = size
    random.seed(seed,0)
    # use same seed each time for testing purposed

    grid = [[False for j in range(SIZE)] for i in range(SIZE)]
    # initialize all places to open, i.e., they can be visited
    for i in range(SIZE):
        for j in range(SIZE):
            x = random.uniform(0.0,1.0)
            # generate a random number
            if x < prob:
                grid[i][j] = True
                # makes the palce inaccessible
            else:
                grid[i][j] = False
                # the place remains accessible
    grid[0][0] = False
    # the upper left corner must be accessible
    grid[SIZE-1][SIZE-1] = False
    # lower right corner must be accessible
    return grid


def make_random_cost():
    '''
    Makes the random costs for visiting a place in the grid
    :return: the cost array
    '''
    cost = [[random.choice([1, 2, 3, 4, 5]) for j in range(SIZE)] for i in range(SIZE)]
    # generate the cost matrix using integer values from 1 to 5 as costs
    return cost


# a constant defining the size of the grid

THE_GRID = make_random_grid(100)
# the grid to be used in testing algorithms

THE_COST = make_random_cost()
# the cost matrix to be used in testing algorithms

def legal_place(i, j):
    '''
    Checks if coordinates i and j indicate legal places in the grid
    :param i: row number
    :param j: column number
    :return: true if place is legal
    '''
    if i < 0 or i >= SIZE:
        return False
    if j < 0 or j >= SIZE:
        return False
    return not THE_GRID[i][j]


def is_goal(i, j):
    '''
    checks if coordinates i and are at the goal position
    :param i: row number
    :param j: column number
    :return: true if in goal position
    '''
    return i == SIZE-1 and j == SIZE-1