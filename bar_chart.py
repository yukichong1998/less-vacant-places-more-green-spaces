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
                    margin=dict(l=20, r=20, t=30, b=20),
                    title=y_param,
                    xaxis_title="",
                    yaxis_title="",
                    font={'size':9}
                    )
    return fig
