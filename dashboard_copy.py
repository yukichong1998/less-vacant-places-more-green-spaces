import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import json
import data_cleaning as dc

app = Dash(__name__)

df = pd.read_csv("dummy_data.csv")

HEALTH_COLS = ["stcotr_fips", "est"]

physical_distress = dc.load_health_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_health_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_health_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_health_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_health_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

HEALTH_DATA = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)
HEALTH_DATA = HEALTH_DATA.astype({"census_tract": str})

with open("data/Parks.geojson") as json_file:
        parks = json.load(json_file)

merged_dfs = dc.merge_all_dfs()
table_df = dc.tract_to_neighborhood(merged_dfs)

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
#print(HEALTH_DATA.head())


# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([

    html.H1("Less Parking More Parks", style={'text-align': 'center'}),

    html.H5("Select at least one health indicator."),
    html.Div([
        "Health Indicator(s): ",
        dcc.Dropdown(id="health_inputs",
                options={
                    "Mental Distress" : "Mental Distress",
                    "Physical Distress": "Physical Distress",
                    "Diabetes": "Diabetes",
                    "High Blood Pressure": "High Blood Pressure",
                    "Life Expectancy": "Life Expectancy"
                    },
                multi=True
                )
            ]),
            
    html.Div(id="health_output"),
    html.Br(),
    html.H6("Select at least one census tract."),
    html.Div([dcc.Dropdown(id="tracts",
            options=HEALTH_DATA.census_tract,
            multi=True
            ),
            html.H6("Select at least one health indicator."),
            html.Div([dcc.Checklist(id="health_inputs_checklist",
                    options={
                        "Mental Distress" : "Mental Distress",
                        "Physical Distress": "Physical Distress",
                        "Diabetes": "Diabetes",
                        "High Blood Pressure": "High Blood Pressure",
                        "Life Expectancy": "Life Expectancy"
                        },
                    value = ["Life Expectancy"]
                )
            ])
        ]),

    html.Br(),
    html.Div([dcc.Dropdown(id="slct_year",
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

    html.Div([dcc.Graph(id='chicago_map', figure={}, style={'display': 'inline-block'}),
    dcc.Graph(figure=fig2, style={'display': 'inline-block'}),
    dcc.Graph(figure=fig3, style={'display': 'inline-block'})]),

    dcc.Checklist(id="parks",
                    options={
                        "data/Parks.geojson" : "parks"
                        },
                    value = ["data/Parks.geojson"]
    )
    ]),
    # TABLE
    html.Br(),
    html.Div(dash_table.DataTable(data=, 
                                columns=[{"name": i, "id": i} for i in df.columns],
                                style_cell={'fontSize':20, 'font-family':'sans-serif', 'padding': '5px'},
                                style_header={'fontWeight': 'bold'},))
    ])


# ------------------------------------------------------------------------------
@app.callback(




@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='chicago_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    container = "The parameter chosen by user was: {}".format(option_slctd)

    with open('Neighborhoods.geojson') as fin:
        neighborhoods = json.load(fin)

    fig1 = px.choropleth_mapbox(df, geojson=neighborhoods, locations='sec_neigh', 
                            featureidkey="properties.sec_neigh", 
                            color=option_slctd,
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            mapbox_style="carto-positron",
                            zoom=9, center = {"lat": 41.8, "lon": -87.7},
                            opacity=0.5,
                            labels={'dummy':option_slctd}
                          )
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  
    return container, fig1

# @app.callback(
#     [Output(component_id='parks_map', component_property='figure')],
#     [Input(component_id='parks', component_property='value')])

# def new_graph(shapes):
#     print(shapes[0])

#     with open(shapes[0]) as json_file:
#         parks = json.load(json_file)

#     fig2 = go.Figure(data=[go.Scattermapbox(lat=[0], lon=[0])])

#     # if shapes == 'parks':
#     #     shp = parks

#     fig2.update_layout(
#         margin={"r":0,"t":0,"l":0,"b":0},
#         mapbox=go.layout.Mapbox(
#             style="carto-positron", 
#             zoom=10, 
#             center_lat = 41.8,
#             center_lon = -87.7,
#             layers=[{
#                 'sourcetype': 'geojson',
#                 'source': parks,
#                 'type': "fill",
#             }]
        
#         )
#     )
#     return fig2


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)