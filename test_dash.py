from dash import Dash, dcc, html, Input, Output, dash_table
from dash.dependencies import Input, Output
import data_cleaning as dc
import compute_health_score as chs
import pandas as pd
from functools import reduce

#load data
merged_dfs = dc.merge_all_dfs()
df = dc.tract_to_neighborhood(merged_dfs)

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
        options=df.Neighborhood,
        multi=True),
    dash_table.DataTable(
        id='filtered_table',
        #data=final_df.to_dict('records'),
        #filter_action="native",
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'fontSize':20, 'font-family':'sans-serif', 'padding': '5px'},
        style_header={'fontWeight': 'bold'}),
    
])

# -----------------------------------------
@app.callback(
            Output(component_id='filtered_table', component_property='data'),
            Input(component_id='health_inputs', component_property='value'),
            Input(component_id='neighborhood', component_property='value'))
def filter_table(health_inputs, neighborhood):
    full_df = chs.build_full_df(health_inputs)
    filtered_data = chs.filter_df(full_df, health_inputs, neighborhood)
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