"""
This module contains the ListRecursion class which is focused on the problem
of flattening a nested array. An example of the problem is to flatten the list
[1, 2, 3, [4, 5, [6, 7, 8, 9, [10, 11, 12, 13, 14]]], 15] which would result in
the answer [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].
It investigates a recursive and an iterative approach to flatten the list,
showing that the recursive approach fails for larger nesting depths, due to
the Python recursion limit.


which can be used to generate
a list of lists of a specified nesting depth that can be flattened.  It has
a recursive approach that fails for higher nesting depths due to the Python
recursion limit.  It also has an iterative approach that works for higher
nesting depths, by employing a stack.

"""
from random import randint
from collections import deque
from typing import List


class ListRecursion:
    """
    Class that can be used to generate a list of lists of a specified
    nesting depth that can be flattened.  It has a recursive approach
    that fails for higher nesting depths due to the Python recursion
    limit.  It also has an iterative approach that works for higher
    nesting depths, by employing a stack.

    Usage:
    >>> list_recursion = ListRecursion(4)
    >>> print(list_recursion.the_list)
    [1, 2, 3, [4, 5, [6, 7, 8, 9, [10, 11, 12, 13, 14]]], 15]
    >>> list_recursion.flatten_recursive()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    >> list_recursion.flatten_stack()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


    """
    def __init__(self, length: int) -> None:
        self.length = length
        self.the_list = self.create_list()

    def create_list(self) -> list:
        """
        Create a list with random values of length self.length, each value
        being between 1 and 10.  Note we do this iteratively as recursion
        would blow up for the sizes we are going to use.

        In the case of a depth of 0 or below being asked for we use a depth of
        1.

        :return: list of random values
        """
        the_list = []
        idx = self.add_elements(the_list, self.length > 1)
        current_list = the_list[idx]
        counter = self.length - 1
        while counter > 0:
            idx = self.add_elements(current_list, counter > 1)
            current_list = current_list[idx]
            counter -= 1

        return the_list

    @staticmethod
    def add_elements(the_list: List, add_new_list: bool = True) -> int:
        """
        Populates a list with 5 elements.  If we are going to create a sublist
        then add_new_list must be True, and then we create four integers
        and one list, with the list being in a random position within the list.

        :param the_list: the list that will be populated
        :param add_new_list: True if we are going to create a sublist
        :return: the index of the list element
        """

        # We put the list in the elements at a random index to make the dataset
        # look authentic, so first generate the index to put the list in
        list_idx = randint(0, 4)

        # Now add the elements to the list using a generator and putting a
        # nested list, if we have one, in the index we generated above
        the_list += ([] if idx == list_idx and add_new_list else randint(1, 10)
                     for idx in range(5))

        # We return the index of the list so that the iterative creation
        # of the nested list can move to the next level
        return list_idx


    def flatten_recursive(self, the_list: List = None) -> List[int]:
        """
        Recursively walk through a list of lists and return all the values,
        effectively flattening it.
        This is the recursive approach and so will fail for higher nesting
        depths where the Python recursive limit is breached.

        :param the_list: the list to flatten
        :return: list of the flattened values
        """

        # On initial call we set our target to the the_list member, after that
        # it will be nested lists
        if not the_list:
            the_list = self.the_list
        list_values = []

        # We just want each integer in the list to be flattened and so if it
        # is an integer add it to our results, otherwise we want to recurse
        for element in the_list:
            if type(element) == list:
                if len(element):
                    list_values += self.flatten_recursive(element)
            else:
                list_values.append(element)

        return list_values


    def flatten_stack(self) -> List:
        """
        Walk through a list of lists stored as the the_list member of the class
        and return all the values, effectively flattening it.  This is the
        approach using a stack and so works for higher nesting depths.  Note
        that we use deque as it is faster for stack operations than lists


        :return: list of the flattened values
        """
        list_values = deque()
        list_queue = deque(self.the_list)

        # Take value from the stack and if it is a value then add it to results
        # otherwise unpack the values and add back to the stack for processing
        # effectively iteratively walking through the list
        while list_queue:
            element = list_queue.popleft()
            if type(element) == list:
                for value in reversed(element):
                    list_queue.appendleft(value)
            else:
                list_values.append(element)

        return list(list_values)
