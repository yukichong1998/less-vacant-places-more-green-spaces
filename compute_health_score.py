'''
Compute Health Score
'''
import pandas as pd
import data_cleaning as dc


HEALTH_COLS = ["stcotr_fips", "est"]
physical_distress = dc.load_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")


merged_dfs = dc.merge_all_dfs()
df = dc.tract_to_neighborhood(merged_dfs)

AVG_LIFE_EXP = life_expectancy["Life Expectancy"].mean()
HEALTH_INDICATORS = ["Physical Distress", "Mental Distress", "Diabetes", 
                    "High Blood Pressure", "Life Expectancy"]
OTHER_INDICATORS = ["Hardship Score"]
                    
def compute_health_score(df, metrics):
    if "Life Expectancy" in metrics:
        # subset["relative_life_exp"] = AVG_LIFE_EXP - df["Life Expectancy"]
        # Weight metrics by whether life expectancy is above or below the mean
        early_death = df["Life Expectancy"] < AVG_LIFE_EXP
        df.loc[early_death, metrics] = df.loc[early_death, metrics] * 1.1
        metrics.remove("Life Expectancy")

    weight = 100 / len(metrics)
    subset = df[metrics] / 100 * weight
    subset["Health Risk Score"] = subset[metrics].sum(axis=1).round(1)
    return subset["Health Risk Score"]

def append_health_score(df, metrics):
    '''
    Adds health risk score to the table.
    '''
    health_score = compute_health_score(df, metrics).tolist()
    df['Health Risk Score'] = health_score
    return df

def filter_df(df, metrics, neighborhood):
    cols_to_keep = ["Neighborhood", "Health Risk Score"] + metrics + OTHER_INDICATORS
    subset = df[cols_to_keep]
    subset = subset[subset["Neighborhood"].isin(neighborhood)]
    return subset


    
    # # normalize the data to mean zero
    # mean_score = df["health_score"].mean()
    # std_score = df["health_score"].std()

    # # multiply by negative 1 so the lower values are worse
    # df["health_score_norm"] = -1 * ((df["health_score"] - mean_score) / std_score)

    # subset["summary_score"] = sum([subset[i] for i in metrics])


