from dash import Dash, dcc, html, Input, Output, dash_table
from dash.dependencies import Input, Output
import data_cleaning as dc
import compute_health_score as chs
import pandas as pd
from functools import reduce

#load data
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
HARDSHIP_COLS = ["GEOID", "HDX_2015-2019"]
HARDSHIP_FILENAME = 'hardship_index.csv'
HEALTH_COLS = ["stcotr_fips", "est"]

# Load hardship and health dataframes
ct_data = dc.load_data(CENSUS_TRACT_FILENAME, CENSUS_TRACT_COLS)
ca_data = dc.load_data(COMM_AREA_FILENAME, COMM_AREA_COLS)
hardship = dc.load_data(HARDSHIP_FILENAME, HARDSHIP_COLS)
physical_distress = dc.load_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

# Merge hardship and health dataframes
indicator_dfs = [hardship, physical_distress, mental_distress, diabetes, hbp, life_expectancy]
merged_indicator_dfs = reduce(lambda left,right: pd.merge(left,right,on='census_tract'), indicator_dfs)
df_comm_area = pd.merge(merged_indicator_dfs, ct_data, on="census_tract")
final_df = pd.merge(df_comm_area, ca_data, on="community_area")

app = Dash(__name__)

app.layout = html.Div([
    html.H6("Select at least one health indicator."),
    dcc.Checklist(
        id="health_inputs",
        options={
                "Mental Distress" : "Mental Distress",
                "Physical Distress": "Physical Distress",
                "Diabetes": "Diabetes",
                "High Blood Pressure": "High Blood Pressure",
                "Life Expectancy": "Life Expectancy"
                }
    ),
    # html.Div(id="health_output"),
    # html.Br(),
    html.H6("Select at least one neighborhood."),
    dcc.Dropdown(
        id="neighborhood",
        options=ca_data.Neighborhood,
        multi=True),
    dash_table.DataTable(
        id='filtered_table',
        #data=final_df.to_dict('records'),
        #filter_action="native",
        columns=[{"name": i, "id": i} for i in final_df.columns],
        style_cell={'fontSize':20, 'font-family':'sans-serif', 'padding': '5px'},
        style_header={'fontWeight': 'bold'}),
    
])

# -----------------------------------------
@app.callback(
            Output(component_id='filtered_table', component_property='data'),
            Input(component_id='health_inputs', component_property='value'),
            Input(component_id='neighborhood', component_property='value'))
def filter_table(health_inputs, neighborhood):
    filtered_data = chs.filter_df(health_inputs, neighborhood)
    return filtered_data.to_dict('records')



'''
@app.callback(
            Output(component_id='table', component_property='children'),
            [Input(component_id='health_inputs', component_property='value')],
            [Input(component_id='neighborhood', component_property='value')],
)
def update_health_output(health_inputs, neighborhood):
    if health_inputs:
        s = "summary score: {}".format(dc.create_summary_score(final_df, health_inputs, neighborhood))
        return s
'''

#sudo fuser -k 8050/tcp

if __name__ == '__main__':
    app.run_server(debug=True)