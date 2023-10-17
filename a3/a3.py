"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

Starter code.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""

from typing import TextIO
import statistics

from constants import (CityData, ID, HT, TOTAL, LOW_INCOME,
                       SEP, HT_ID_COL, LI_ID_COL,
                       HT_NBH_NAME_COL, LI_NBH_NAME_COL,
                       HT_20_44_COL, NBH_20_44_COL,
                       HT_45_64_COL, NBH_45_64_COL,
                       HT_65_UP_COL, NBH_65_UP_COL,
                       POP_COL, LI_POP_COL,
                       HT_20_44_IDX, HT_45_64_IDX, HT_65_UP_IDX,
                       NBH_20_44_IDX, NBH_45_64_IDX, NBH_65_UP_IDX
                       )

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

SAMPLE_DATA1 = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [703, 13291, 3741, 9663, 3959, 5176]},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [789, 12906, 3578, 8815, 2927, 3902]}
}
SAMPLE_DATA2 = {
    'West Humber-Clairville': {
        'id': 1,
        'total': 33230, 'low_income': 5950},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'total': 32940, 'low_income': 9690},

}
SAMPLE_DATA3 = {
    'West Humber-Clairville': {
        'id': 1,
        'total': 33230, 'low_income': 5950},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'total': 33230, 'low_income': 9690},

}

EPSILON = 0.005


# This function is provided for use in Task 3. You do not need to
# change it.  Note the use of EPSILON constant (similar to what we had
# in asisgnment 2) for testing.
def get_age_standardized_ht_rate(city_data: CityData, nbh_name: str) -> float:
    """Return the age standardized hypertension rate from the
    neighbourhood in city_data with neighbourhood name nbh_name.

    Precondition: nbh_name is in city_data

    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Elms-Old Rexdale') -
    ...     24.44627) < EPSILON
    True
    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Rexdale-Kipling') -
    ...     24.72562) < EPSILON
    True

    """

    rates = calculate_ht_rates_by_age_group(city_data, nbh_name)

    # These rates are normalized for only 20+ ages, using the census data
    # that our datasets are based on.
    canada_20_44 = 11_199_830 / 19_735_665  # Number of 20-44 / Number of 20+
    canada_45_64 = 5_365_865 / 19_735_665  # Number of 45-64 / Number of 20+
    canada_65_plus = 3_169_970 / 19_735_665  # Number of 65+ / Number of 20+

    return (rates[0] * canada_20_44 + rates[1] * canada_45_64 +
            rates[2] * canada_65_plus)


def get_bigger_neighbourhood(city_data: CityData,
                             neigh1: str, neigh2: str) -> str:
    '''Return the higher population between neigh1 and neigh2 from city_data,
    according to the low income data. If a neighbourhood is not in city_data,
    assume the population is 0. If the population is the same, return the
    neighbourhood that comes first in city_data.

    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Elms-Old Rexdale',
    ...                          'Rexdale-Kipling')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'West Humber-Clairville',
    ...                          'Thistletown-Beaumond Heights')
    'West Humber-Clairville'
    '''
    if neigh1 in city_data and neigh2 in city_data:
        if city_data[neigh1][TOTAL] > city_data[neigh2][TOTAL]:
            return neigh1
        if city_data[neigh1][TOTAL] == city_data[neigh2][TOTAL]:
            return neigh1
        return neigh2
    if neigh1 not in city_data and neigh2 not in city_data:
        return neigh1
    if neigh1 not in city_data and neigh2 in city_data:
        return neigh2
    return neigh1


def get_high_hypertension_rate(city_data: CityData,
                               threshold: float) -> list[tuple]:
    '''Return a list of tuples containing all neighbourhoods with a
    hypertension rate greater than or equal to threshold.

    >>> result = get_high_hypertension_rate(SAMPLE_DATA, 0.3)
    >>> result == [('Thistletown-Beaumond Heights', 0.31797739151574084),
    ...            ('Rexdale-Kipling', 0.3117001828153565)]
    True
    >>> result = get_high_hypertension_rate(SAMPLE_DATA, 0.2)
    >>> result == [('West Humber-Clairville', 0.2987202275151084),
    ...            ('Mount Olive-Silverstone-Jamestown', 0.28466612028255867),
    ...            ('Thistletown-Beaumond Heights', 0.31797739151574084),
    ...            ('Rexdale-Kipling', 0.3117001828153565),
    ...            ('Elms-Old Rexdale', 0.2878808035120394)]
    True
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.5)
    []
    '''
    high_hype = []
    for item in city_data:
        total_hype = city_data[item][HT][HT_20_44_IDX] + \
            city_data[item][HT][HT_45_64_IDX] + \
            city_data[item][HT][HT_65_UP_IDX]
        total_adults = city_data[item][HT][NBH_20_44_IDX] + \
            city_data[item][HT][NBH_45_64_IDX] + \
            city_data[item][HT][NBH_65_UP_IDX]
        hype_rate = total_hype / total_adults
        if hype_rate >= threshold:
            high_hype.append(tuple([item, hype_rate]))
    return high_hype


def hype_low_ratio(city_data: CityData, city: str) -> float:
    '''Return a ratio between the hypertension rate and low
    income rate from city in city_data.

    >>> hype_low_ratio(SAMPLE_DATA, 'West Humber-Clairville')
    1.6683148168616895
    >>> hype_low_ratio(SAMPLE_DATA, 'Mount Olive-Silverstone-Jamestown')
    0.9676885451091314
    '''
    total_hype = city_data[city][HT][HT_20_44_IDX] + \
        city_data[city][HT][HT_45_64_IDX] + \
        city_data[city][HT][HT_65_UP_IDX]
    total_adults = city_data[city][HT][NBH_20_44_IDX] + \
        city_data[city][HT][NBH_45_64_IDX] + \
        city_data[city][HT][NBH_65_UP_IDX]
    hype_rate = total_hype / total_adults
    low_rate = city_data[city][LOW_INCOME] / city_data[city][TOTAL]
    return hype_rate / low_rate


def get_ht_to_low_income_ratios(city_data: CityData) -> dict[str, float]:
    '''Return a dict containing the ratio of the hypertension rate and
    the low income rate of the cities in city_data.

    >>> result = get_ht_to_low_income_ratios(SAMPLE_DATA)
    >>> result == {'West Humber-Clairville': 1.6683148168616895,
    ...            'Mount Olive-Silverstone-Jamestown': 0.9676885451091314,
    ...            'Thistletown-Beaumond Heights': 1.6438083107534431,
    ...            'Rexdale-Kipling': 1.5351962275111484,
    ...            'Elms-Old Rexdale': 1.1763941257986577}
    True
    '''
    ht_low_dict = {}
    for item in city_data:
        ht_low_dict[item] = hype_low_ratio(city_data, item)
    return ht_low_dict


def calculate_ht_rates_by_age_group(city_data: CityData, neigh: str
                                    ) -> tuple([float, float, float]):
    '''Return a tuple containing three floats, which are the hypertension
    rates of each of the age groups from neigh in city_data.

    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'West Humber-Clairville')
    (5.289293506884358, 38.71468488047191, 76.48763523956723)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Elms-Old Rexdale')
    (5.24903071875932, 36.593947923997185, 71.70953101361573)
    '''
    age_1 = (city_data[neigh][HT][HT_20_44_IDX] /
             city_data[neigh][HT][NBH_20_44_IDX]) * 100
    age_2 = (city_data[neigh][HT][HT_45_64_IDX] /
             city_data[neigh][HT][NBH_45_64_IDX]) * 100
    age_3 = (city_data[neigh][HT][HT_65_UP_IDX] /
             city_data[neigh][HT][NBH_65_UP_IDX]) * 100
    return tuple([age_1, age_2, age_3])


def get_correlation(city_data: CityData) -> float:
    '''Return the correlation between age standardised hypertension rates
    and low income rates across all neighbourhoods.

    >>> get_correlation(SAMPLE_DATA)
    0.28509539188554994

    '''
    low_income = []
    age_standard = []
    for item in city_data:
        li_data = city_data[item][LOW_INCOME] / city_data[item][TOTAL]
        as_data = get_age_standardized_ht_rate(city_data, item)
        low_income.append(li_data)
        age_standard.append(as_data)
    return statistics.correlation(low_income, age_standard)


def age_standard_list(city_data: CityData) -> list[float]:
    '''Return a list of the age-standardized hit rates from the
    neighbourhoods in city_data.

    >>> result = age_standard_list(SAMPLE_DATA)
    >>> result == [25.81318996667875, 26.553843121654182, 25.763294160369608,
    ...            24.72562462246556, 24.44627521389894]
    True
    '''
    new = []
    for item in city_data:
        new.append(get_age_standardized_ht_rate(city_data, item))
    return new


def low_total(city_data: CityData) -> list[float]:
    '''Return a list of the low_income rates from the neighbourhoods
    in city_data.

    >>> result = low_total(SAMPLE_DATA)
    >>> result == [0.1790550707192296, 0.2941712204007286, 0.19343945972021226,
    ...            0.2030360531309298, 0.24471458773784355]
    True
    '''
    new = []
    for item in city_data:
        new.append(city_data[item][LOW_INCOME] / city_data[item][TOTAL])
    return new


def order_by_ht_rate(city_data: CityData) -> list[str]:
    '''Return a list of the names of the neighbourhoods in city_data, sorted by
    age-standardized hypertension rate, from least to greatest.

    >>> result = order_by_ht_rate(SAMPLE_DATA)
    >>> result == ['Elms-Old Rexdale', 'Rexdale-Kipling',
    ...            'Thistletown-Beaumond Heights', 'West Humber-Clairville',
    ...            'Mount Olive-Silverstone-Jamestown']
    True

    '''
    ht_rate = age_standard_list(SAMPLE_DATA)
    ht_rate.sort()
    neighbourhoods = []
    for item in ht_rate:
        for item1 in city_data:
            if get_age_standardized_ht_rate(SAMPLE_DATA, item1) == item:
                neighbourhoods.append(item1)
    return neighbourhoods


def get_hypertension_data(data: dict, file: TextIO) -> None:
    '''Modify dict to include the hypertension data in file.

    '''
    hypeline = file.readlines()[1:]
    for line in hypeline:
        new = line.split(SEP)
        if new[HT_NBH_NAME_COL] in data:
            data[new[HT_NBH_NAME_COL]][HT] = [int(new[HT_20_44_COL]),
                                              int(new[NBH_20_44_COL]),
                                              int(new[HT_45_64_COL]),
                                              int(new[NBH_45_64_COL]),
                                              int(new[HT_65_UP_COL]),
                                              int(new[NBH_65_UP_COL].strip())]
        else:
            data[new[HT_NBH_NAME_COL]] = {ID: int(new[HT_ID_COL]),
                                          HT: [int(new[HT_20_44_COL]),
                                               int(new[NBH_20_44_COL]),
                                               int(new[HT_45_64_COL]),
                                               int(new[NBH_45_64_COL]),
                                               int(new[HT_65_UP_COL]),
                                               int(new[NBH_65_UP_COL].strip())]
                                          }


def get_low_income_data(data: dict, file: TextIO) -> None:
    '''Modify dict to include the low income data in file.

    '''
    incline = file.readlines()[1:]
    for line in incline:
        new = line.split(SEP)
        if new[LI_NBH_NAME_COL] in data:
            data[new[LI_NBH_NAME_COL]][LOW_INCOME] = int(new[LI_POP_COL])
            data[new[LI_NBH_NAME_COL]][TOTAL] = int(new[POP_COL])
        if new[LI_NBH_NAME_COL] not in data:
            data[new[LI_NBH_NAME_COL]] = {ID: int(new[LI_ID_COL]),
                                          TOTAL: int(new[POP_COL]),
                                          LOW_INCOME: int(new[LI_POP_COL])
                                          }


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment when ready to test:
    # Using the small data files:
    small_data = {}
    # add hypertension data
    with open('/Users/mealadebadi/Downloads/a3/hypertension_data_small.csv') \
         as ht_small_f:
        get_hypertension_data(small_data, ht_small_f)
    # add low income data
    with open('/Users/mealadebadi/Downloads/a3/low_income_small.csv') \
         as li_small_f:
        get_low_income_data(small_data, li_small_f)

    print('Did we build the dict correctly?', small_data == SAMPLE_DATA)
    print('Correlation in small data file:', get_correlation(small_data))

    # Using the example data files:
    example_neighbourhood_data = {}
    # add hypertension data
    with open('/Users/mealadebadi/Downloads/a3/hypertension_data_2016.csv') \
         as ht_example_f:
        get_hypertension_data(example_neighbourhood_data, ht_example_f)
    # add low income data
    with open('/Users/mealadebadi/Downloads/a3/low_income_2016.csv') as \
         li_example_f:
        get_low_income_data(example_neighbourhood_data, li_example_f)
    print('Correlation in example data file:',
          get_correlation(example_neighbourhood_data))
