import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import json

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("dummy_data.csv")

print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "Health", "value": "Health"},
                     {"label": "Green Spaces", "value": "Green"},
                     {"label": "Open Lots", "value": "Lots"}],
                 multi=False,
                 value="Health",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The parameter chosen by user was: {}".format(option_slctd)

    with open('Neighborhoods.geojson') as fin:
        neighborhoods = json.load(fin)

    fig = px.choropleth_mapbox(df, geojson=neighborhoods, locations='sec_neigh', featureidkey="properties.sec_neigh", color=option_slctd,
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=9, center = {"lat": 41.8, "lon": -87.7},
                           opacity=0.5,
                           labels={'dummy':option_slctd}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)