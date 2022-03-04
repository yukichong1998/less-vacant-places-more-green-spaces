'''
This module handles the data cleaning process.
'''

import pandas as pd

PARKS_COLS = ["PARK", "LOCATION", "ZIP", "ACRES", "PARK_CLASS"]
PARKS_FILENAME = 'CPD_Parks.csv'

HARDSHIP_COLS = ["GEOID", "HDX_2015-2019"]
VAR_NAMES = {
    "GEOID":"census_tract",
    "HDX_2015-2019":"Hardship Score",
    }
HARDSHIP_FILENAME = 'hardship_index.csv'

HEALTH_COLS = ["stcotr_fips", "est"]


def load_data(filename, col_list):
    df = pd.read_csv(filename, header=0, usecols=col_list)
    df = df.rename(columns=VAR_NAMES)
    return df


def load_health_data(filename, col_list, col_name=None):
    df = pd.read_csv(filename, header=0, usecols=col_list)
    if col_name:
        df = df.rename(columns = {"stcotr_fips":"census_tract", "est": col_name})
    return df

# Parks data
parks = load_data(PARKS_FILENAME, PARKS_COLS)
parks = parks.astype({"ZIP": str, "ACRES": float})

# Hardship index
hardship = load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)

# Health data
physical_distress = load_health_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = load_health_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = load_health_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = load_health_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = load_health_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

health_data = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)
health_data = health_data.astype({"census_tract": str})
#Although each set has 803 rows, when merged, there are 823 rows. Why?


# Creating summary score of health indicators    
def create_summary_score(data, metrics, tracts):
    '''
    Given the selected health metrics and tracts, creates a subset of
    data and a new column for summary score.

    Inputs:
        data: a dataframe consisting of one column for each health indicator
                and a column for tract.
        tracts: list of tracts (str) to filter for
        metrics: list of health indicators (str) to filter for
    '''
    filter_tract = data["census_tract"].isin(tracts)
    cols_to_keep = ["census_tract"] + metrics
    subset = data.loc[filter_tract, cols_to_keep]
    print("subset:", subset)

    subset["summary_score"] = sum([subset[i] for i in metrics])
    return subset



