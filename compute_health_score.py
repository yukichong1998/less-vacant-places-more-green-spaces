'''
Compute Health Score
'''
import pandas as pd
import data_cleaning as dc

CENSUS_TRACT_COLS = ["GEOID10", "COMMAREA"]
CENSUS_TRACT_FILENAME = 'census_tracts.csv'
COMM_AREA_COLS = ["AREA_NUMBER", "COMMUNITY"]
COMM_AREA_FILENAME = 'comm_areas.csv'
ct_data = dc.load_data(CENSUS_TRACT_FILENAME, CENSUS_TRACT_COLS)
ca_data = dc.load_data(COMM_AREA_FILENAME, COMM_AREA_COLS)

HEALTH_COLS = ["stcotr_fips", "est"]
physical_distress = dc.load_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

def agg_health_df():
    '''
    Builds an aggregated dataframe with all the health indicators and 
    '''
    merge_health_dfs()

def merge_health_dfs():
    '''
    Builds a dataframe with all the health indicators by census tract
    '''
    health_df = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)

    return health_df

AVG_LIFE_EXP = life_expectancy["Life Expectancy"].mean()
HEALTH_INDICATORS = ["Physical Distress", "Mental Distress", "Diabetes", 
                    "High Blood Pressure", "Life Expectancy"]
def compute_health_score(df, metrics, neighborhood):
    filter_neighborhood = df["Neighborhood"].isin(neighborhood)
    cols_to_keep = ["Neighborhood"] + metrics
    subset = df.loc[filter_neighborhood, cols_to_keep]
    if "Life Expectancy" in metrics:
        df["Life Expectancy"] = AVG_LIFE_EXP - df["Life Expectancy"]
    df["health_score"] = df[metrics].mean(axis=1)
    
    # normalize the data to mean zero and set up the "adversity index"
    mean_score = df["health_score"].mean()
    std_score = df["health_score"].std()

    # multiply by negative 1 so the lower values are worse
    df["health_score_norm"] = -1 * ((df["health_score"] - mean_score) / std_score)

    # subset["summary_score"] = sum([subset[i] for i in metrics])


