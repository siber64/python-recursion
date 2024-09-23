"""

"""

from collections import defaultdict
import pytest
from scripts.list_recursion import ListRecursion


@pytest.mark.parametrize("depth", [0, 1, 14, 2000])
def test_list_recursion_create_list(depth):
    """
    Test that the list is created correctly of the form with 4 integers and 1
    sublist per level, except for the final level that has 5 integers

    :param depth: The nesting depth of the list
    :return:
    """
    list_recursion = ListRecursion(depth)
    the_list = list_recursion.the_list
    while depth:
        idx_by_type = defaultdict(list)
        for idx, val in enumerate(the_list):
            idx_by_type[type(val)].append(idx)
        if depth == 1:
            assert len(idx_by_type[int]) == 5
        else:
            assert len(idx_by_type[int]) == 4
            assert len(idx_by_type[list]) == 1
            the_list = the_list[idx_by_type[list][0]]

        depth -= 1


@pytest.mark.parametrize("nested_list, flat_list_limit",
         ( ([1, 2, 3, [4, 5, [6, 7, 8, 9, [10, 11, 12, 13, 14], 15]]], 15),
           ([[]], 0),([], 0),([[],[1,2],[]], 2) # Check handles empty lists
         )
         )
def test_list_recursion_flatten(mocker, nested_list, flat_list_limit):
    """
    Test that the list is flattened correctly using the recursive and stack
    approach and
    check that it manages empty lists in various configurations

    :param mocker: mocker fixture
    :param nested_list: The list that will be flattened
    :param flat_list_limit: The limit of the flattened list to generate a
    list                    sequence that will be the expected result
    :return:
    """
    # Override the creation so that we can assert the result
    mocker.patch.object(ListRecursion, "create_list", return_value=nested_list)
    list_recursion = ListRecursion(4)
    flat_values_recursive = list_recursion.flatten_recursive()
    flat_values_stack = list_recursion.flatten_stack()
    assert flat_values_recursive == flat_values_stack == [i for i in range (1, flat_list_limit + 1)]


def test_list_recursion_flatten_recursive_too_big():
    """
    This test demonstrates that the recursive approach will fail if the nesting
    depth is too big for the Python recursion limit

    :param mocker: mocker fixture
    :return:
    """
    list_recursion = ListRecursion(1000)
    with pytest.raises(RecursionError):
        list_recursion.flatten_recursive()


@pytest.mark.parametrize("depth", [0, 1, 14, 2000])
def test_list_recursion_flatten_stack(mocker, depth):
    """
    Test that the list is flattened correctly using the iterative approach
    adn that it can handle depths too big for the recursive approach

    Note that we override the randint function so that we can control the
    values created and assert the end result

    :param mocker: mocker fixture
    :param depth:
    :return:
    """
    # this block creates an infinite generator of ordered positive integers
    # for use in overriding randint() so that the flattened list is ordered
    # correctly for easy assertion
    sequence_number = 1

    def infinite_sequence():
        nonlocal sequence_number
        while True:
            yield sequence_number
            sequence_number += 1

    numbers = infinite_sequence()

    # This is the override for randint() that has two new behaviours.  When
    # the limit for the random integer is 4 then we are generating the random
    # index for the list position, so we always make this 4 making sublist
    # the last element of the list meaning when we flatten we get consecutive
    # integers to test.  Else we are generating an integer element of the
    # list and we want this to be the next in the sequence of positive integers
    # so that we can assert the end result

    def randint_mock(*args):
        if args[1] == 4:
            result = 4
        else:
            result = next(numbers)
        return result

    mocker.patch('scripts.list_recursion.randint', side_effect=randint_mock)
    list_recursion = ListRecursion(depth)
    flat_values = list_recursion.flatten_stack()
    assert flat_values == [i for i in range(1, (
        list_recursion.length if list_recursion.length > 0 else 1) * 4 + 2)]
