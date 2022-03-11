import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  
import json
import compute_health_score as chs

app = Dash(__name__)

df = pd.read_csv('data/zoom.csv')
print(df)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_parameter",
                 options=[
                     {"label": "Parks", "value": "Parks"},
                     {"label": "Lots", "value": "Lots"}],
                 multi=False,
                 value="Parks",
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id="slct_neigh",
                 options=[
                     {"label": "A", "value": "A"},
                     {"label": "B", "value": "B"}],
                 multi=False,
                 value="Parks",
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
    [Input(component_id='slct_parameter', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The parameter chosen by user was: {}".format(option_slctd)

    with open("data/Parks.geojson") as json_file:
        parks = json.load(json_file)

    fig2 = go.Figure(data=[go.Scattermapbox(lat=[0], lon=[0])])

        # if shapes == 'parks':
        #     shp = parks

    fig2.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox=go.layout.Mapbox(
                style="carto-positron", 
                zoom=10, 
                center_lat = 41.8,
                center_lon = -87.7,
                layers=[{
                    'sourcetype': 'geojson',
                    'source': parks,
                    'type': "fill",
                    'color': 'royalblue'
                }]
            
            )
        )

    fig3 = go.Figure(data=[go.Scattermapbox(lat=[0], lon=[0])])

        # if shapes == 'parks':
        #     shp = parks

    fig3.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox=go.layout.Mapbox(
                style="carto-positron", 
                zoom=10, 
                center_lat = 41.8,
                center_lon = -87.7,
                layers=[{
                    'sourcetype': 'geojson',
                    'source': parks,
                    'type': "fill"
                }]
            
            )
        )

    if option_slctd == "Lots":
        return container, fig3  
    return container, fig2

#sudo fuser -k 8050/tcp

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)