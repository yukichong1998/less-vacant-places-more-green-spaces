import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  
import json
import data_cleaning as dc
import compute_health_score as chs

app = Dash(__name__)

# HEALTH_COLS = ["stcotr_fips", "est"]
# life_expectancy = dc.load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")
# AVG_LIFE_EXP = life_expectancy["Life Expectancy"].mean()
# HEALTH_INDICATORS = ["Physical Distress", "Mental Distress", "Diabetes", 
#                     "High Blood Pressure", "Life Expectancy"]
# OTHER_INDICATORS = ["Hardship Score"]

# merged_dfs = dc.merge_all_dfs()
# df = dc.tract_to_neighborhood(merged_dfs)

# print(df.head())


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_parameter",
                 options=[
                     {"label": "Hardship Score", "value": "Hardship Score"},
                     {"label": "Health Risk Score", "value": "Health Risk Score"},
                     {"label": "Number of Vacant Lots", "value": "Vacant Lots"},
                     {"label": "Number of Green Spaces", "value": "Number of Green Spaces"},
                     {"label": "Area of Green Spaces", "value": "Area of Green Spaces"}],
                 multi=False,
                 value="Hardship Score",
                 style={'width': "40%"}
                 ),

    html.Div([dcc.Checklist(id="health_inputs_checklist",
                    options={
                        "Mental Distress" : "Mental Distress",
                        "Physical Distress": "Physical Distress",
                        "Diabetes": "Diabetes",
                        "High Blood Pressure": "High Blood Pressure",
                        "Life Expectancy": "Life Expectancy"
                        },
                    value = ["Mental Distress"]
                )]),
    
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='chicago_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='chicago_map', component_property='figure')],
    [Input(component_id='slct_parameter', component_property='value'),
    Input(component_id='health_inputs_checklist', component_property='value')]
)
def update_graph(option_slctd, health_params):
    print(option_slctd)
    print(type(option_slctd))
    print(health_params)

    container = "The parameter chosen by user was: {}".format(option_slctd)

    with open('Community Areas.geojson') as fin:
        neighborhoods = json.load(fin)

    df = chs.build_full_df(health_params)
    print(df.columns)


    fig = px.choropleth_mapbox(df, geojson=neighborhoods, locations='Neighborhood', 
                            featureidkey="properties.community", 
                            color=option_slctd,
                            color_continuous_scale="algae",
                            mapbox_style="carto-positron",
                            zoom=9, center = {"lat": 41.81, "lon": -87.7},
                            opacity=0.5,
                            labels={'df':option_slctd}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  
    return container, fig

#sudo fuser -k 8050/tcp

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)