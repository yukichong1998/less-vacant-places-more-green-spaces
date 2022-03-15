import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  
import json
import scatterplot_data as sd


app = Dash(__name__)

boundaries = sd.neighborhood_zoom()
df = sd.scatter_data()

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    dcc.Checklist(id="slct_parameter",
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
    Input(component_id='slct_neigh', component_property='value')]
)
def update_graph(option_slctd, neigh_slct):

    container = "Parks and Vacant Lot Locations"

    if "Vacant Lots" not in option_slctd:
        data = df[df['type'] == "Park"]
    elif "Parks" not in option_slctd:
        data = df[df['type'] == "Vacant Lot"]
    else:
        data = df

    print(data.head())

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

#sudo fuser -k 8050/tcp

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)