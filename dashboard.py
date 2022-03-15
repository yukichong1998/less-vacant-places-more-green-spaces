import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import json
import compute_health_score as chs
import scatterplot_data as sd

pd.options.mode.chained_assignment = None

app = Dash(__name__)

boundaries = sd.neighborhood_zoom()
scatter_df = sd.scatter_data()
table_cols = ["Neighborhood", "Hardship Score", 
            "Mental Distress", 
            "Physical Distress", 
            "Diabetes", 
            "High Blood Pressure", 
            "Life Expectancy", 
            "Health Risk Score", 
            "Vacant Lots", 
            "Number of Green Spaces", 
            "Area of Green Spaces"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    html.Div([
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

        dcc.Checklist(id="health_inputs_checklist",
                    options={
                        "Mental Distress" : "Mental Distress",
                        "Physical Distress": "Physical Distress",
                        "Diabetes": "Diabetes",
                        "High Blood Pressure": "High Blood Pressure",
                        "Life Expectancy": "Life Expectancy"
                        },
                    value = ["Mental Distress", "Life Expectancy"]
                ),
    
        html.Div(id='output_container1', children=[]),
        html.Br(),

        dcc.Graph(id='chicago_map_choro', figure={},
        style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Checklist(id="slct_locations",
             options={
                    "Parks": "Parks",
                    "Vacant Lots": "Vacant Lots"
                        },
                value = ["Parks", "Vacant Lots"]
                ),
    
        dcc.Dropdown(id="slct_neigh",
                 options=boundaries.index,
                 multi=False,
                 value="CHICAGO",
                 style={'width': "40%"}
                 ),

     
        html.Div(id='output_container2', children=[]),
        html.Br(),

        dcc.Graph(id='chicago_map_scatter', figure={},
        style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Div(id='output_container3', children=[]),
        dcc.Graph(id='bar', figure={},
        style={'width': '49%', 'display': 'inline-block'})    
    ]),

    html.Div([
        dash_table.DataTable(id='table', columns=[{'id': c, 'name': c} for c in table_cols]) 
    ])
 

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='chicago_map_choro', component_property='figure')],
    [Input(component_id='slct_parameter', component_property='value'),
    Input(component_id='health_inputs_checklist', component_property='value')]
)
def update_choro(option_slctd, health_params):

    container = "The parameter chosen by user was: {}".format(option_slctd)

    with open('Community_Areas.geojson') as fin:
        neighborhoods = json.load(fin)

    choro_df = chs.build_full_df(health_params)
   
    fig = px.choropleth_mapbox(choro_df, geojson=neighborhoods, locations='Neighborhood', 
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

@app.callback(
    [Output(component_id='output_container2', component_property='children'),
     Output(component_id='chicago_map_scatter', component_property='figure')],
    [Input(component_id='slct_locations', component_property='value'),
    Input(component_id='slct_neigh', component_property='value')]
)
def update_scatter(option_slctd, neigh_slct):

    container = "Parks and Vacant Lot Locations"

    if "Vacant Lots" not in option_slctd:
        data = scatter_df[scatter_df['type'] == "Park"]
    elif "Parks" not in option_slctd:
        data = scatter_df[scatter_df['type'] == "Vacant Lot"]
    else:
        data = scatter_df

    zoom_opt = boundaries.loc[neigh_slct]["Zoom"]
    lat_opt = boundaries.loc[neigh_slct]["Lat"]
    lon_opt = boundaries.loc[neigh_slct]["Lon"]

    with open('Community_Areas.geojson') as fin:
        neighborhoods = json.load(fin)

    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="type", hover_name="name", hover_data=["community_area_name"], 
                            color_discrete_map={"Park":"green", "Vacant Lot":"gray"})
    fig.update_layout(mapbox=go.layout.Mapbox(
                    style="carto-positron",
                    zoom=zoom_opt, 
                    center_lat = lat_opt,
                    center_lon = lon_opt,
                    layers=[{
                        'sourcetype': 'geojson',
                        'source': neighborhoods,
                        'type': "line",
                        'opacity': 0.5
                    }]))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return container, fig

@app.callback(
    [Output(component_id='output_container3', component_property='children'),
     Output(component_id='bar', component_property='figure')],
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value')]
)

def update_bar(health_params, neigh_slct):
    data = chs.build_full_df(health_params)
    data.set_index('Neighborhood', inplace=True)
    cols_to_mean = [c for c in table_cols if c != "Neighborhood"]
    data.loc['CHICAGO'] = data[cols_to_mean].mean()

    bar_x = ['Hardship Score', 'Health Risk Score', 'Number of Green Spaces', 'Number of Vacant Lots']
    bar_y = [data['Hardship Score'].loc[neigh_slct], 
            data['Health Risk Score'].loc[neigh_slct], 
            data['Number of Green Spaces'].loc[neigh_slct], 
            data['Vacant Lots'].loc[neigh_slct]]

    container = []

    fig = px.bar(data, x=bar_x, y=bar_y)

    return container, fig

@app.callback(Output(component_id='table', component_property='data'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value')]
)

def update_table(health_params, neigh_selct):
    data = chs.build_full_df(health_params)
    cols_to_mean = [c for c in table_cols if c != "Neighborhood"]
    data.loc['mean'] = data[cols_to_mean].mean()
    data['Neighborhood'].loc['mean'] = 'CHICAGO'

    output = data[data["Neighborhood"] == neigh_selct]
    output = output.round(2)
    
    return output.to_dict('records')



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)