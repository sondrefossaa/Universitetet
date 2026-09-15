'''
    Class representing a guest in a constraint satisfaction problem
    Written by Bjornar Tessem, 28. August 2020
'''


class Guest:
    '''
    A representation of a guest in the invitation CSP
    '''

    NOT_INVITED = 0
    INVITED = 1
    UNDECIDED = 2

    def __init__(self, name, invited = UNDECIDED):
        '''
        Constructor for the Guest object
        :param name: the name of a guest
        :param invited: invitation status for a guest
        '''
        self.name = name
        self.invited = invited

    # some checks for invitation status
    def is_invited(self):
        return self.invited == Guest.INVITED

    def is_not_invited(self):
        return self.invited == Guest.NOT_INVITED

    def is_undecided(self):
        return self.invited == Guest.UNDECIDED

    def __eq__(self, other):
        '''
        :param other: a Guest node to compare with
        :return: True if self and other have the same name
        '''
        return self.name == other.name
