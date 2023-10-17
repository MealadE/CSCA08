"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

Constants used in a3.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""
from typing import Union

# NbhData type (values for CityData). Nbh stands for "neighbourhood".
NbhData = dict[str, Union[int, list[int]]]
# NbhData keys
ID = 'id'
HT = 'hypertension'
TOTAL = 'total'
LOW_INCOME = 'low_income'

# CityData type: keys are neighbourhood names, values are
# neighbourhood data.
CityData = dict[str, NbhData]


# the separator used in the input files
SEP = ','

# Columns in the neighbourhood hypertension file.
HT_ID_COL = 0        # An ID that uniquely identifies each neighbourhood.
HT_NBH_NAME_COL = 1  # The (unique) name of the neighbourhood.
# The number of people aged 20 to 44 with hypertension in the neighbourhood.
HT_20_44_COL = 2
# The total number of people aged 20 to 44 in the neighbourhood.
NBH_20_44_COL = 3
# The number of people aged 45 to 64 with hypertension in the neighbourhood.
HT_45_64_COL = 4
# The total number of people aged 45 to 64 in the neighbourhood.
NBH_45_64_COL = 5
# The number of people aged 65 and older with hypertension in the neighbourhood.
HT_65_UP_COL = 6
# The total number of people aged 65 and older in the neighbourhood.
NBH_65_UP_COL = 7

# Columns in the neighbourhood income file.
LI_ID_COL = 0        # An ID that uniquely identifies each neighbourhood.
LI_NBH_NAME_COL = 1  # The (unique) name of the neighbourhood.
POP_COL = 2          # The total population in the neighbourhood.
# The number of people in the neighbourhood with low income status.
LI_POP_COL = 3

# The indices at which we store hypertension data.
HT_20_44_IDX = 0
NBH_20_44_IDX = 1
HT_45_64_IDX = 2
NBH_45_64_IDX = 3
HT_65_UP_IDX = 4
NBH_65_UP_IDX = 5
