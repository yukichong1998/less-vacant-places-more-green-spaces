'''
This module handles the data cleaning process.
'''

import pandas as pd

PARKS_COLS = ["PARK", "LOCATION", "ZIP", "ACRES", "PARK_CLASS"]
PARKS_FILENAME = 'CPD_Parks.csv'


def load_data(filename, col_list, col_name=None):
    df = pd.read_csv(filename, header=0, usecols=col_list)
    if col_name:
        df = df.rename(columns = {"est": col_name})
    return df


parks = load_data(PARKS_FILENAME, PARKS_COLS)

# Data cleaning
parks = parks.astype({"ZIP": str, "ACRES": float})


HEALTH_COLS = ["tract_code", "est"]
mental_distress = load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

health_data = mental_distress.merge(diabetes).merge(hbp).merge(life_expectancy)
health_data = health_data.astype({"tract_code": str})
#Although each set has 803 rows, when merged, there are 823 rows. Why?

# Creating summary score of health indicators    
def create_summary_score(data, metrics, tracts, weights=None):
    '''
    Calculates a summary score given weights selected by the user for
    each of the four health indicators and the selected tract(s).

    Inputs:
        data: a dataframe consisting of one column for each health indicator
                and a column for tract.
        tracts: list of tracts (str) to filter for
        metrics: list of health indicators (str) to filter for
        weights: tuple of four int as weights for each column
    '''
    filter_tract = data["tract_code"].isin(tracts)
    cols_to_keep = ["tract_code"] + metrics
    subset = data.loc[filter_tract, cols_to_keep]

    rv = subset.sum(axis=1)
    return f"summary score = {rv}"





