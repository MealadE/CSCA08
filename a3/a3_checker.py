"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

A simple checker for functions in a3.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""

from io import StringIO
from typing import Any, Union
import unittest
import checker
import a3

CONSTANTS = {
    'ID': 'id',
    'HT': 'hypertension',
    'TOTAL': 'total',
    'LOW_INCOME': 'low_income',
    'SEP': ',',
    'HT_ID_COL': 0,
    'HT_NBH_NAME_COL': 1,
    'HT_20_44_COL': 2,
    'NBH_20_44_COL': 3,
    'HT_45_64_COL': 4,
    'NBH_45_64_COL': 5,
    'HT_65_UP_COL': 6,
    'NBH_65_UP_COL': 7,
    'LI_ID_COL': 0,
    'LI_NBH_NAME_COL': 1,
    'POP_COL': 2,
    'LI_POP_COL': 3,
    'HT_20_44_IDX': 0,
    'NBH_20_44_IDX': 1,
    'HT_45_64_IDX': 2,
    'NBH_45_64_IDX': 3,
    'HT_65_UP_IDX': 4,
    'NBH_65_UP_IDX': 5
}

SAMPLE_DATA = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [703, 13291, 3741, 9663, 3959, 5176],
        'total': 33230, 'low_income': 5950},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [789, 12906, 3578, 8815, 2927, 3902],
        'total': 32940, 'low_income': 9690},
    'Thistletown-Beaumond Heights': {
        'id': 3,
        'hypertension': [220, 3631, 1047, 2829, 1349, 1767],
        'total': 10365, 'low_income': 2005},
    'Rexdale-Kipling': {
        'id': 4,
        'hypertension': [201, 3669, 1134, 3229, 1393, 1854],
        'total': 10540, 'low_income': 2140},
    'Elms-Old Rexdale': {
        'id': 5,
        'hypertension': [176, 3353, 1040, 2842, 948, 1322],
        'total': 9460, 'low_income': 2315}
}

HT_DATA_SMALL = '''Neighbourhood ID,Neighbourhood Name,# of people with hypertension 2016/17 (Age 20-44),Total Population 2016 (Age 20-44),# of people with hypertension 2016/17 (Age 45-64),Total Population 2016 (Age 45-64),# of people with hypertension 2016/17 (Age 65+),Total Population 2016 (Age 65+)
1,West Humber-Clairville,703,13291,3741,9663,3959,5176
2,Mount Olive-Silverstone-Jamestown,789,12906,3578,8815,2927,3902
3,Thistletown-Beaumond Heights,220,3631,1047,2829,1349,1767
4,Rexdale-Kipling,201,3669,1134,3229,1393,1854
5,Elms-Old Rexdale,176,3353,1040,2842,948,1322
'''

LI_DATA_SMALL = '''Neighb ID,Neighbourhood Name,Total - Population (Denominator),"Total - In Low Income MBM"
1,West Humber-Clairville,33230,5950
2,Mount Olive-Silverstone-Jamestown,32940,9690
3,Thistletown-Beaumond Heights,10365,2005
4,Rexdale-Kipling,10540,2140
5,Elms-Old Rexdale,9460,2315
'''


class TestChecker(unittest.TestCase):
    """Sanity checker for assignment 3 functions."""

    def test_get_hypertension_data(self) -> None:
        """Function get_hypertension_data"""

        self._check(a3.get_hypertension_data, [{}, StringIO(HT_DATA_SMALL)],
                    type(None))

    def test_get_low_income_data(self) -> None:
        """Function get_low_income_data"""

        self._check(a3.get_low_income_data, [{}, StringIO(LI_DATA_SMALL)],
                    type(None))

    def test_get_bigger_neighbourhood(self) -> None:
        """Function get_bigger_neighbourhood"""

        self._check(a3.get_bigger_neighbourhood,
                    [SAMPLE_DATA,
                     'Mount Olive-Silverstone-Jamestown',
                     'Rexdale-Kipling'],
                    str)

    def test_get_high_hypertension_rate(self) -> None:
        """Function get_high_hypertension_rate"""

        print(f'\nChecking get_high_hypertension_rate...')
        result = checker.returns_list_of(
            a3.get_high_hypertension_rate, [SAMPLE_DATA, 0.24], tuple)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def test_get_ht_to_low_income_ratios(self) -> None:
        """Function get_ht_to_low_income_ratios"""

        self._check(a3.get_ht_to_low_income_ratios,
                    [SAMPLE_DATA], dict)

    def test_calculate_ht_rates_by_age_group(self) -> None:
        """Function calculate_ht_rates_by_age_group"""

        print('\nChecking calculate_ht_rates_by_age_group...')
        result = checker.returns_tuple_of(
            a3.calculate_ht_rates_by_age_group,
            [SAMPLE_DATA,
             'Elms-Old Rexdale'],
            (float, float, float))
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def test_get_correlation(self) -> None:
        """Function get_correlation"""

        self._check(a3.get_correlation, [SAMPLE_DATA], float)

    def test_order_by_ht_rate(self) -> None:
        """Function order_by_ht_rate"""

        print('\nChecking order_by_ht_rate...')
        result = checker.returns_list_of(a3.order_by_ht_rate,
                                         [SAMPLE_DATA], str)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, a3)
        print('  check complete')

    def _check(self, func: callable, args: list, ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print(f'\nChecking {func.__name__}...')
        result = checker.type_check_simple(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_constants(self, name2value: dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = (f'The value of constant {name} should be '
                   '{expected} but is {actual}.')
            self.assertEqual(expected, actual, msg)


checker.ensure_no_io('a3')
TARGET_LEN = 79
print(''.center(TARGET_LEN, "="))
print(' Start: checking coding style '.center(TARGET_LEN, "="))
checker.run_pyta('a3.py', 'pyta/a3_pyta.txt')
print(' End checking coding style '.center(TARGET_LEN, "="))

print(' Start: checking type contracts '.center(TARGET_LEN, "="))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, "="))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
