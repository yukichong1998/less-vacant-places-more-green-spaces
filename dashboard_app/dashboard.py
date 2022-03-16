'''
Module creating the interactive dashboard
'''

import pandas as pd
import json
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate
import data_prep.compute_health_score as chs
import data_viz.scatterplot_data as sd
import data_prep.data_cleaning as dc
import data_viz.bar_chart as bar_chart

pd.options.mode.chained_assignment = None
df = dc.tract_to_neighborhood()

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

boundaries = sd.neighborhood_zoom()
scatter_df = sd.scatter_data()
TABLE_COLS = ["Neighborhood", "Hardship Score", 
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
    html.Div([
        html.P(children="🌳🌳🌳", className="header-emoji"),
        html.H1("Less Vacant Places, More Green Spaces", style={'text-align': 'center'}, className="header-title"),
        html.P(
            children="Analyzing the effect of green spaces on public health",
            className="header-description")],
            className="header"),
    html.Br(),
    html.Div([html.Div([html.H3("Distribution across Neighborhoods in Chicago", className="map-title"),
                        html.Br(),
                        html.H4("Select a map layer:", className="subheader-title"),
                        dcc.Dropdown(id="slct_parameter",
                                options=[
                                    {"label": "Hardship Score", "value": "Hardship Score"},
                                    {"label": "Health Risk Score", "value": "Health Risk Score"},
                                    {"label": "Number of Vacant Lots", "value": "Vacant Lots"},
                                    {"label": "Number of Green Spaces", "value": "Number of Green Spaces"},
                                    {"label": "Area of Green Spaces", "value": "Area of Green Spaces"}],
                                multi=False,
                                value="Hardship Score",
                                style={'width': "70%"}),
                        
                        html.Br(),
                        
                        html.Div(id='health_inputs_container',
                                children = [html.H4("Select at least two health indicators to compute the health risk score.", className="subheader-title"),
                                            dcc.Checklist(
                                                id="health_inputs_checklist",
                                                options={
                                                    "Mental Distress" : "Mental Distress",
                                                    "Physical Distress": "Physical Distress",
                                                    "Diabetes": "Diabetes",
                                                    "High Blood Pressure": "High Blood Pressure",
                                                    "Life Expectancy": "Life Expectancy"
                                                    },
                                                value = ["Mental Distress", "Life Expectancy"],
                                                className="checklist"
                                            )],
                                style= {'width': '50%', 'display': 'block'}
                                )],
                        style= {'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
            html.Div([
                html.H3("Locations of Parks and Vacant Lots", className="map-title"),
                html.Br(),
                html.H4("Select a neighborhood:", className="subheader-title"),
                dcc.Dropdown(id="slct_neigh",
                        options=boundaries.index,
                        multi=False,
                        value="CHICAGO",
                        style={'width': "50%"},
                        ),
                dcc.Checklist(
                    id="slct_locations",
                    options={
                            "Parks": "Parks",
                            "Vacant Lots": "Vacant Lots"
                                },
                    value = ["Parks", "Vacant Lots"],
                    className="checklist"
                        ),
            ],
            style= {'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}
        )
        ]
    ),

    html.Br(),

    html.Div([dcc.Graph(id='chicago_map_choro', figure={},
                style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='chicago_map_scatter', figure={},
                style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Br(),

    html.H3("Legend:", className="map-title"),
    html.H4("Hardship Score - Composite score incorporating unemployment," 
            "age dependency, education, per capita income, crowded housing," 
            "and poverty into a single score", className="subheader-title"),
    html.H4("Health Risk Score -  Composite score incorporating at least two of" 
            "the following metrics selected:", className="subheader-title"),
    html.H5("   - Mental Distress: Mental health not good for ≥14 days during the past 30 days among adults aged ≥18 years (%)", className="checklist"),
    html.H5("   - Physical Distress: Physical health not good for ≥14 days during the past 30 days among adults aged ≥18 years (%)", className="checklist"),
    html.H5("   - Diabetes: Diabetes among adults aged ≥18 years (%)", className="checklist"),
    html.H5("   - High Blood Pressure: High blood pressure among adults aged ≥18 years (%)", className="checklist"),
    html.H5("   - Life Expectancy: Average life expectancy at birth (years)", className="checklist"),
    html.H4("Area of Green Spaces (acres)", className="subheader-title"),

    html.Br(),

    html.H3("Comparison between Neighborhoods", className="map-title"),
    html.H4("Select a neighborhood to compare with.", className="subheader-title"),

    html.Br(),

    dcc.Dropdown(id="slct_second_neigh",
            style={'width': "40%"}
            ),

    html.Br(),

    html.Div([
            dcc.Graph(id='bar_hardship', figure={},
                style={'width': '20%', 'display': 'inline-block'}),
            dcc.Graph(id='bar_healthrisk', figure={},
                style={'width': '20%', 'display': 'inline-block'}),
            dcc.Graph(id='bar_vacantlots', figure={},
                style={'width': '20%', 'display': 'inline-block'}),
            dcc.Graph(id='bar_greenspaces', figure={},
                style={'width': '20%', 'display': 'inline-block'}),
            dcc.Graph(id='bar_areagreenspaces', figure={},
                style={'width': '20%', 'display': 'inline-block'})
    ]),

    html.Br(),

    html.Div([
        dash_table.DataTable(
            id='table',
            style_cell={
                'fontSize':14, 
                'font-family': 'sans-serif', 
                'padding': '5px', 
                'color': 'rgb(246, 234, 223)',
                'backgroundColor': 'transparent'},
            style_header={'fontWeight': 'bold'}
            )
    ]),

    html.Br()],

    style={'margin-left':'25px',
            'margin-right':'25px',
            'margin-bottom':'30px',
            'margin-top':'30px'}
)


# ------------------------------------------------------------------------------
# Update graph showing distribution of selected parameter across Chicago
@app.callback(
    Output(component_id='chicago_map_choro', component_property='figure'),
    [Input(component_id='slct_parameter', component_property='value'),
    Input(component_id='health_inputs_checklist', component_property='value')]
)
def update_choro(option_slctd, health_params):
    if not option_slctd:
        raise PreventUpdate
    else:
        with open('data_prep/data/Community_Areas.geojson') as fin:
            neighborhoods = json.load(fin)

        choro_df = chs.append_health_score(df, health_params)
    
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
    
        return fig

# Checklist for selecting health indicators to be included in calculation
# of Health Risk Score is dependent on selection of Health Risk Score as
# a map layer
@app.callback(
    Output(component_id='health_inputs_container', component_property='style'),
    Input(component_id='slct_parameter', component_property='value'))
def show_health_inputs_checklist(parameter):
    if not parameter:
        raise PreventUpdate
    else:
        if "Health Risk Score" in parameter:
            return {'display': 'block'}
        else:
            return {'display':'none'}

# Update graph showing locations of green spaces and/or vacant lots
# for a selected neighborhood
@app.callback(
    Output(component_id='chicago_map_scatter', component_property='figure'),
    [Input(component_id='slct_locations', component_property='value'),
    Input(component_id='slct_neigh', component_property='value')]
)
def update_scatter(option_slctd, neigh_slct):
    if not neigh_slct:
        raise PreventUpdate
    else:
        if "Vacant Lots" not in option_slctd:
            data = scatter_df[scatter_df['Land Use'] == "Park"]
        elif "Parks" not in option_slctd:
            data = scatter_df[scatter_df['Land Use'] == "Vacant Lot"]
        else:
            data = scatter_df

        zoom_opt = boundaries.loc[neigh_slct]["Zoom"]
        lat_opt = boundaries.loc[neigh_slct]["Lat"]
        lon_opt = boundaries.loc[neigh_slct]["Lon"]

        with open('data_prep/data/Community_Areas.geojson') as fin:
            neighborhoods = json.load(fin)

        fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="Land Use", hover_name="name", hover_data=["community_area_name"], 
                                color_discrete_map={"Park":"green", "Vacant Lot":"gray"}, size='normalized_size')
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

        return fig

# Update dropdown list options for selecting a second neighborhood to
# exclude the first selected neighborhood
@app.callback(
    Output(component_id='slct_second_neigh', component_property='options'),
    Input(component_id='slct_neigh', component_property='value')
    )
def update_second_neigh(first_neigh):
    neighborhoods = [neigh for neigh in boundaries.index if neigh != first_neigh and neigh != 'CHICAGO']
    return neighborhoods

# Bar chart for Hardship Score
@app.callback(
    Output(component_id='bar_hardship', component_property='figure'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_hardship_bar(health_params, first_neigh, second_neigh):
    if not second_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        return bar_chart.create_bar_chart(data, health_params, (first_neigh, second_neigh), 'Hardship Score')

# Bar chart for Health Risk Score
@app.callback(
    Output(component_id='bar_healthrisk', component_property='figure'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_healthrisk_bar(health_params, first_neigh, second_neigh):
    if not second_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        return bar_chart.create_bar_chart(data, health_params, (first_neigh, second_neigh), 'Health Risk Score')

# Bar chart for Vacant Lots
@app.callback(
    Output(component_id='bar_vacantlots', component_property='figure'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_vacantlots_bar(health_params, first_neigh, second_neigh):
    if not second_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        return bar_chart.create_bar_chart(data, health_params, (first_neigh, second_neigh), 'Vacant Lots')

# Bar chart for Green Spaces
@app.callback(
    Output(component_id='bar_greenspaces', component_property='figure'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_greenspaces_bar(health_params, first_neigh, second_neigh):
    if not second_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        return bar_chart.create_bar_chart(data, health_params, (first_neigh, second_neigh), 'Number of Green Spaces')

# Bar chart for Area of Green Spaces
@app.callback(
    Output(component_id='bar_areagreenspaces', component_property='figure'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_areagreenspaces_bar(health_params, first_neigh, second_neigh):
    if not second_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        return bar_chart.create_bar_chart(data, health_params, (first_neigh, second_neigh), 'Area of Green Spaces')

# Table of all indicators for selected neighborhood and health indicators
@app.callback(Output(component_id='table', component_property='data'),
    [Input(component_id='health_inputs_checklist', component_property='value'),
    Input(component_id='slct_neigh', component_property='value'),
    Input(component_id='slct_second_neigh', component_property='value')]
)
def update_table(health_params, first_neigh, second_neigh):
    if not first_neigh:
        raise PreventUpdate
    else:
        data = chs.append_health_score(df, health_params)
        if first_neigh == 'CHICAGO':
            cols_to_mean = [c for c in TABLE_COLS if c != "Neighborhood"]
            data.loc['mean'] = data[cols_to_mean].mean()
            data['Neighborhood'].loc['mean'] = 'CHICAGO'
        output = chs.filter_df(data, health_params, [first_neigh, second_neigh])
        output = output.round(2)

        return output.to_dict('records')


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)