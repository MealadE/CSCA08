"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

Starter code for tests to test function get_bigger_neighbourhood in
a3.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""

import copy
import unittest
from a3 import get_bigger_neighbourhood as gbn
from a3 import SAMPLE_DATA
from a3 import SAMPLE_DATA3


class TestGetBiggerNeighbourhood(unittest.TestCase):
    """Test the function get_bigger_neighbourhood."""

    def test_first_bigger(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is strictly greater than the
        population of the second neighbourhood.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'Elms-Old Rexdale')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_second_bigger(self):
        '''Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when its population is strictly greater than the population
        of the second neighbourhood.

        '''
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_no_mutation(self):
        expected = copy.deepcopy(SAMPLE_DATA)
        actual = SAMPLE_DATA
        gbn(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling')
        msg = ("gbn(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling') \
        modified the input!" + "We expected the input to stay " \
               + str(expected) + ", but found it changed to " + str(actual))        
        self.assertEqual(actual, expected, msg)
        
    def test_both_same(self):
        '''Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is the exact same as the population
        of the second neighbourhood and the first neighbourhood appears before
        the second neighbourhood in the dictionary.

        '''
        sample_data_copy = copy.deepcopy(SAMPLE_DATA3)
        expected = 'West Humber-Clairville'
        actual = gbn(SAMPLE_DATA3, 'West Humber-Clairville', 
                     'Mount Olive-Silverstone-Jamestown')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_first_zero(self):
        '''Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when the first neighbourhood is not in the dictionary
        while the second neighbourhood is.

        '''
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Toronto', 'Rexdale-Kipling')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_second_zero(self):
        '''Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when the second neighbourhood is not in the dictionary
        while the first neighbourhood is.

        '''
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'Toronto')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_both_not(self):
        '''Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when both neighbourhoods are not in the dictionary.

        '''
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Ajax'
        actual = gbn(SAMPLE_DATA, 'Ajax', 'Toronto')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
