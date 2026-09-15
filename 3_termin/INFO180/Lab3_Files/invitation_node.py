'''
    Class for representing a node in a search tree for the invitation problem
    Written by Bjornar Tessem, 28.08 2020
    Modified 02.09.2024
'''
import copy
from guest import Guest


class InvitationNode:
    '''
        The class represents the node in a search tree for the invitation csp
    '''

    def __init__(self):
        '''
             A constructor that represent the state of the csp problem at a particular node
        '''
        # Normally one would not hard code data in to a program, but sometimes simplicity is
        # the easiest way to do thing
        # Here you should add all the guests that might be relevant for your party
        # according to the pattern on the next lines
        self.anne = Guest("Anne")
        self.ola = Guest("Ola")
        self.jan = Guest("Jan")

        # You also need to make a list of all these potential guests
        self.assignment = [self.anne, self.ola, self.jan]

    def get_neighbours(self):
        '''
            Finds the consistent children of a node in the search tree
        :return: a list of children
        '''
        result = []

        n = self.copy_and_add_assignment(Guest.INVITED)
        # generate a child where the next undecided guest is tested for invitation
        if n is not None and n.is_consistent():
            # if there is such a guest and i the invitation assignment is consistent then append n
            result.append(n)

        n = self.copy_and_add_assignment(Guest.NOT_INVITED)
        # generate a child where the next undecided guest is tested for not invitation
        if n is not None and n.is_consistent():
            # if there is such a guest and i the invitation assignment is consistent then append n
            result.append(n)

        return result

    def copy_and_add_assignment(self,invite):
        '''
        Copys a node and adds one invitation status to one potential guest
        :param invite: the invitation status to set
        :return: a node with invitation set for one more guest
        '''
        new_node = copy.deepcopy(self)
        # copy the node
        for guest in new_node.assignment:
            # find a guest that is undecided in self's assignment
            if guest.is_undecided():
                # set this particular guests invitation status to 'invite'
                guest.invited = invite
                return new_node
        return None

    def is_consistent(self):
        '''
        The function that checks if assignments are consistent
        :return: True if an assignment is consistent with the constraints otherwise False
        '''
        val = True
        # Here we add all the constraints
        # This should not be hardcoded in more serious CSP programs.
        #
        # The idea is that only relevant constraints for consistency should be checked.
        # To be relevant the node needs to have an assignment that is not UNDECIDED for any of the guests in
        # the constraint. We check this by using the none_undecided('list of guest objects') method.

        # The parameter to a use of that method should be the guests involved in the constraint in
        # the if-block defining the constraint
        # So every constraint here should be of the form
        # if self.none_undecided('list of guests in constraint'):
        #   constraint_n = <some constraint as a boolean expression in python>
        #   val = val and constrain_n
        # Look at the example constraints already there
        # Perhaps a bit hard to read, but it works ...

        # anne => ~ola <=> ~anne or ~ola
        if self.none_undecided([self.anne, self.ola]):
            constraint_1 = (self.anne.is_not_invited() or self.ola.is_not_invited())
            val = val and constraint_1

        # anne => jan <=> ~anne or jan
        if self.none_undecided([self.anne, self.jan]):
            constraint_2= self.anne.is_not_invited() or self.jan.is_invited()
            val = val and constraint_2

        # ~anne => ~jan <=> anne or ~jan
        if self.none_undecided([self.anne, self.jan]):
            constraint_3 = self.anne.is_invited() or self.jan.is_not_invited()
            val = val and constraint_3

        # check how many invited so far
        constraint_4 = self.is_ok_guest_count()
        val = val and constraint_4

        return val

    def is_ok_guest_count(self):
        count_invited = 0
        count_undecided = 0
        for guest in self.assignment:
            if guest.is_invited():
                count_invited = count_invited + 1
            elif guest.is_undecided():
                count_undecided = count_undecided + 1
        # wants at least 0 and at most 3 guests
        return (count_invited <= 3 and count_invited + count_undecided >= 0)


    def none_undecided(self, constraint_guests):
        '''
        Local function that checks that all guests in a constraint are not UNDECIDED
        :param constraint_guests: the guests involved in a constraint
        :return: False if some guests in the list is UNDECIDED
        '''
        val = True
        for g in constraint_guests:
            if g.is_undecided():
                val = False
        return val

    def is_goal(self):
        '''
        Checks if we are at a goal/leaf in the search tree
        :return: True if all guests have been DECIDED
        '''
        for guest in self.assignment:
            if guest.is_undecided():
                return False
        return True

    def __str__(self):
        '''
        :return: A string representation of an Invitation Node
        '''
        str = ''
        for g in self.assignment:
            if g.invited == Guest.INVITED:
                status = "Invited"
            elif g.invited == Guest.NOT_INVITED:
                status = "Not invited"
            elif g.invited == Guest.UNDECIDED:
                status == "Undecided"
            str = str + '{:6} {}\n'.format(g.name,status)
        return str

