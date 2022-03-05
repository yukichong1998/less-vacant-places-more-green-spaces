from dash import Dash, dash_table
import pandas as pd
from functools import reduce
import data_cleaning as dc

HARDSHIP_COLS = ["GEOID", "HDX_2015-2019"]
VAR_NAMES = {
    "GEOID":"census_tract",
    "HDX_2015-2019":"Hardship Score",
    }
HARDSHIP_FILENAME = 'hardship_index.csv'

HEALTH_COLS = ["stcotr_fips", "est"]

# def rename_cols(filename):
#     df = pd.read_csv(filename)
#     cols_to_keep = list(VAR_NAMES.keys())
#     df = df[cols_to_keep]
#     final_df = df.rename(columns=VAR_NAMES)
#     return final_df

# Load hardship and health dataframes
hardship = dc.load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)
physical_distress = dc.load_health_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_health_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_health_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_health_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_health_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

# Merge hardship and health dataframes
dfs = [hardship, physical_distress, mental_distress, diabetes, hbp, life_expectancy]
merged_df = reduce(lambda left,right: pd.merge(left,right,on='census_tract'), dfs)

app = Dash(__name__)

app.layout = dash_table.DataTable(
    data=merged_df.to_dict('records'), 
    columns=[{"name": i, "id": i} for i in merged_df.columns],
    style_cell={'fontSize':20, 'font-family':'sans-serif', 'padding': '5px'},
    style_header={'fontWeight': 'bold'},)


if __name__ == '__main__':
    app.run_server(debug=True)