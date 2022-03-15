import plotly.express as px
import compute_health_score as chs

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

COLORS = {"Hardship Score": "#E8B4B8",
        "Health Risk Score": "#EED6D3",
        "Vacant Lots": "#A49393",
        "Number of Green Spaces": "#837126",
        "Area of Green Spaces": "#634F40"
        }

def create_bar_chart(data, health_params, first_neigh, second_neigh, y_param):
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
