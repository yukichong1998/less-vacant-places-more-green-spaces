'''
Module for creating bar charts
'''

import plotly.express as px
import data_prep.compute_health_score as chs

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

COLORS = {"Hardship Score": "#40594C",
        "Health Risk Score": "#855858",
        "Vacant Lots": "#A49393",
        "Number of Green Spaces": "#837126",
        "Area of Green Spaces": "#634F40"
        }

def create_bar_chart(data, health_params, neighborhoods, y_param):
    '''
    Creates a bar chart comparing two neighborhoods on a given y_parameter.
    Inputs:
        data (Pandas DataFrame): full dataset with all columns
        health_params (list of str): health indicators selected by the user
        neighborhoods (tuple of str): two neighborhoods to compare
        y_param (str): the metric to compare the neighborhoods on:
            Hardship Score, Health Risk Score, Vacant Lots, Number of Green Spaces,
            or Area of Green Spaces
    
    Returns: Plotly Express bar chart        
    '''
    first_neigh, second_neigh = neighborhoods
    if first_neigh == "CHICAGO":
        cols_to_mean = [c for c in TABLE_COLS if c != "Neighborhood"]
        data.loc['CHICAGO'] = data[cols_to_mean].mean()

    fltr_data = chs.filter_df(data, health_params, [first_neigh, second_neigh])
    fltr_data.set_index('Neighborhood', inplace=True)
    bar_x = [first_neigh, second_neigh]
    bar_y = [fltr_data[y_param].loc[first_neigh],
            fltr_data[y_param].loc[second_neigh]]
    fig = px.bar(fltr_data, x=bar_x, y=bar_y)
    fig.update_layout(width=300,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=10),
                    title=y_param,
                    xaxis_title="",
                    yaxis_title="",
                    font={'size':10}
                    )
    fig.update_traces(marker_color=COLORS[y_param],
                        width=0.6)
    
    return fig
