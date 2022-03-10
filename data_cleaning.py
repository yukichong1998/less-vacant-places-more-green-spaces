'''
This module handles the data cleaning process.
'''
import numpy as np
import pandas as pd
from functools import reduce

VAR_NAMES = {
    "GEOID":"census_tract",
    "GEOID10":"census_tract",
    "COMMAREA":"community_area",
    "AREA_NUMBER":"community_area",
    "COMMUNITY":"Neighborhood",
    "HDX_2015-2019":"Hardship Score",
    }

CENSUS_TRACT_COLS = ["GEOID10", "COMMAREA"]
CENSUS_TRACT_FILENAME = 'census_tracts.csv'
COMM_AREA_COLS = ["AREA_NUMBER", "COMMUNITY"]
COMM_AREA_FILENAME = 'comm_areas.csv'

PARKS_COLS = ["PARK", "LOCATION", "ZIP", "ACRES", "PARK_CLASS"]
PARKS_FILENAME = 'CPD_Parks.csv'

HARDSHIP_COLS = ["GEOID", "HDX_2015-2019"]
HARDSHIP_FILENAME = 'hardship_index.csv'

HEALTH_COLS = ["stcotr_fips", "est"]
HEALTH_INDICATORS = ["Physical Distress", "Mental Distress", "Diabetes", 
                    "High Blood Pressure", "Life Expectancy"]
ALL_INDICATORS = ["Hardship Score", "Physical Distress", "Mental Distress", 
"Diabetes", "High Blood Pressure", "Life Expectancy"]


def load_data(filename, col_list, col_name=None):
    df = pd.read_csv(filename, header=0, usecols=col_list)
    if col_name:
        df = df.rename(columns = {"stcotr_fips":"census_tract", "est": col_name})
    else:
        df = df.rename(columns=VAR_NAMES)
    return df

# Parks data
parks = load_data(PARKS_FILENAME, PARKS_COLS)
parks = parks.astype({"ZIP": str, "ACRES": float})

# Hardship index
hardship = load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)

def merge_health_dfs():
    '''
    Merges health dataframes on census tract unique identifier and cleans the
    data by replacing empty NaN values with column mean.
    '''
    physical_distress = load_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
    mental_distress = load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
    diabetes = load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
    hbp = load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
    life_expectancy = load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

    health_data = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)
    
    # Replace empty values with column mean
    for i in HEALTH_INDICATORS:
        health_data[i].fillna(health_data[i].mean(), inplace=True)
        health_data[i] = health_data[i].round(1)
    return health_data

def merge_all_dfs():
    '''
    Merges health, hardship, lots and green spaces dataframes on census tract
    unique identifier.
    '''
    hardship = load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)
    health = merge_health_dfs()
    indicator_dfs = [hardship, health]
    merged_df = reduce(lambda left,right: pd.merge(left,right,on='census_tract'), indicator_dfs)
    return merged_df


def tract_to_neighborhood(df):
    '''
    Converts geo-identifier from census tract to community area / neighborhood.
    '''
    ct_data = load_data(CENSUS_TRACT_FILENAME, CENSUS_TRACT_COLS)
    ca_data = load_data(COMM_AREA_FILENAME, COMM_AREA_COLS)
    df_comm_area = pd.merge(df, ct_data, on="census_tract")
    final_df = df_comm_area.groupby('community_area', as_index=False).agg('mean')
    final_df = pd.merge(final_df, ca_data, on="community_area")
    final_df = final_df.loc[:, final_df.columns!='census_tract']
    for col in ALL_INDICATORS:
        final_df[col] = final_df[col].round(1)

    return final_df

 
# def create_summary_score(data, metrics, neighborhood):
#     '''
#     Given the selected health metrics and tracts, creates a subset of
#     data and a new column for summary score.

#     Inputs:
#         data: a dataframe consisting of one column for each health indicator
#                 and a column for tract.
#         tracts: list of tracts (str) to filter for
#         metrics: list of health indicators (str) to filter for
#     '''
#     filter_neighborhood = data["Neighborhood"].isin(neighborhood)
#     cols_to_keep = ["Neighborhood"] + metrics
#     subset = data.loc[filter_neighborhood, cols_to_keep]
#     print("subset:", subset)

#     subset["summary_score"] = sum([subset[i] for i in metrics])
#     print("Health Score:", subset["summary_score"])
#     return subset



