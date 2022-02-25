'''
This module handles the data cleaning process.
'''

import pandas as pd

PARKS_COLS = ["PARK", "LOCATION", "ZIP", "ACRES", "PARK_CLASS"]
PARKS_FILENAME = 'CPD_Parks.csv'


def load_data(filename, col_list):
    df = pd.read_csv(filename, header=0, usecols=col_list)

    return df


parks = load_data(PARKS_FILENAME, PARKS_COLS)

# Data cleaning
parks = parks.astype({"ZIP": str, "ACRES": float})