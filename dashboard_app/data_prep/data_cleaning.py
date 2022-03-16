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
    "vacant_count":"Vacant Lots",
    "park_count":"Number of Green Spaces",
    "park_acres":"Area of Green Spaces"
    }

CENSUS_TRACT_COLS = ["GEOID10", "COMMAREA"]
CENSUS_TRACT_FILENAME = 'data_prep/data/census_tracts.csv'
COMM_AREA_COLS = ["AREA_NUMBER", "COMMUNITY"]
COMM_AREA_FILENAME = 'data_prep/data/comm_areas.csv'

HARDSHIP_COLS = ["GEOID", "HDX_2015-2019"]
HARDSHIP_FILENAME = 'data_prep/data/hardship_index.csv'

PARKS_LOTS_COLS = ["Neighborhood", "vacant_count", "park_count", "park_acres", "park_polygons"]
PARKS_LOTS_FILENAME = 'data_prep/data/community_areas.csv'

HEALTH_COLS = ["stcotr_fips", "est"]
HEALTH_INDICATORS = ["Physical Distress", "Mental Distress", "Diabetes", 
                    "High Blood Pressure", "Life Expectancy"]
ALL_INDICATORS = ["Hardship Score", "Physical Distress", "Mental Distress", 
                "Diabetes", "High Blood Pressure", "Life Expectancy"]


def load_data(filename, col_list, col_name=None):
    '''
    Load csv file and rename columns.
    
    Inputs:
        - filename: (CSV file)
        - col_list: (list) Column names
    
    Returns:
        - (pandas dataframe) Dataframe
    '''
    df = pd.read_csv(filename, header=0, usecols=col_list)
    if col_name:
        df = df.rename(columns = {"stcotr_fips":"census_tract", "est": col_name})
    else:
        df = df.rename(columns=VAR_NAMES)
    return df


def merge_health_dfs():
    '''
    Merges health dataframes on census tract unique identifier and cleans the
    data by replacing empty NaN values with column mean.
    '''
    physical_distress = load_data("data_prep/data/health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
    mental_distress = load_data("data_prep/data/health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
    diabetes = load_data("data_prep/data/health_diabetes.csv", HEALTH_COLS, "Diabetes")
    hbp = load_data("data_prep/data/health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
    life_expectancy = load_data("data_prep/data/health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

    health_data = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)
    
    # Replace empty values with column mean
    for i in HEALTH_INDICATORS:
        health_data[i].fillna(health_data[i].mean(), inplace=True)
        health_data[i] = health_data[i].round(1)
    return health_data


def tract_to_neighborhood():
    '''
    Converts geo-identifier from census tract to community area / neighborhood.
    '''
    ct_data = load_data(CENSUS_TRACT_FILENAME, CENSUS_TRACT_COLS)
    ca_data = load_data(COMM_AREA_FILENAME, COMM_AREA_COLS)
    hardship = load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)
    health = merge_health_dfs()
    parks_lots = load_data(PARKS_LOTS_FILENAME, PARKS_LOTS_COLS)
    dfs_to_merge = [ct_data, hardship, health]
    df = reduce(lambda left,right: pd.merge(left,right,on='census_tract'), dfs_to_merge)
    df = df.groupby('community_area', as_index=False).agg('mean')
    df = pd.merge(df, ca_data, on="community_area")
    df = pd.merge(df, parks_lots, on="Neighborhood")
    df = df.loc[:, df.columns!='census_tract']
    
    for col in ALL_INDICATORS:
        df[col] = df[col].round(1)

    return df

