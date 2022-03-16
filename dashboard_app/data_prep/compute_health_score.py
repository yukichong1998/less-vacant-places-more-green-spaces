'''
Compute Health Score
'''
import pandas as pd
import data_prep.data_cleaning as dc


HEALTH_COLS = ["stcotr_fips", "est"]
life_expectancy = dc.load_data("data_prep/data/health_life_expectancy.csv", HEALTH_COLS, 
                               "Life Expectancy")
AVG_LIFE_EXP = life_expectancy["Life Expectancy"].mean()
OTHER_INDICATORS = ["Hardship Score", "Vacant Lots", "Number of Green Spaces",
                    "Area of Green Spaces"]


def compute_health_score(df, metrics):
    '''
    Computes health risk score for each neighborhood by taking the mean of all 
    the health indicators selected by the user as percentages, then weighting 
    that average more heavily if the life expectancy of this neighborhood is 
    below the average life expectancy in Chicago.
    '''
    assert len(metrics) > 1
    new_metrics = metrics
    if "Life Expectancy" in metrics:
        # Weight metrics by whether life expectancy is above or below the mean
        early_death = df["Life Expectancy"] < AVG_LIFE_EXP
        df.loc[early_death, metrics] = df.loc[early_death, metrics] * 1.1
        new_metrics = [c for c in metrics if c != "Life Expectancy"]
    weight = 100 / len(new_metrics)
    subset = df[new_metrics] / 100 * weight
    subset["Health Risk Score"] = subset[new_metrics].sum(axis=1).round(1)
    return subset["Health Risk Score"]


def append_health_score(df, metrics):
    '''
    Calculates and appends health risk score to the dataframe.
    '''
    health_score = compute_health_score(df, metrics).tolist()
    df['Health Risk Score'] = health_score
    return df


def build_full_df(metrics):
    '''
    Builds full dataframe with all indicators and all 77 neighborhoods.

    Returns:
        - (pandas dataframe) full dataframe
    '''
    df = dc.tract_to_neighborhood()
    full_df = append_health_score(df, metrics)
    return full_df


def filter_df(df, metrics, neighborhood):
    '''
    Filters dataframe by health metrics and neighborhood selected by user.

    Inputs:
        - df: (pandas dataframe)
        - metrics: (list)
        - neighborhood: (list)
    
    Returns:
        - (pandas dataframe) Filtered dataframe by health metrics and 
        neighborhood selected
    '''
    cols_to_keep = ["Neighborhood", "Health Risk Score"] + \
                    metrics + OTHER_INDICATORS
    subset = df[cols_to_keep]
    subset = subset[subset["Neighborhood"].isin(neighborhood)]
    return subset

