from dash import Dash, dcc, html, Input, Output
import data_cleaning as dc

#load data
HEALTH_COLS = ["tract_code", "est"]
mental_distress = dc.load_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

HEALTH_DATA = mental_distress.merge(diabetes).merge(hbp).merge(life_expectancy)
HEALTH_DATA = HEALTH_DATA.astype({"tract_code": str})


app = Dash(__name__)

app.layout = html.Div([
            html.H6("Select at least one health indicator."),
            html.Div([
            "Health Indicator(s): ",
            dcc.Dropdown(id="health_inputs",
                        options={
                                "Mental Distress" : "Mental Distress",
                                "Diabetes": "Diabetes",
                                "High Blood Pressure": "High Blood Pressure",
                                "Life Expectancy": "Life Expectancy"
                        },
                        multi=True
                    )
                ]),
            html.Div(id="health_output"),
            html.Br(),
            html.H6("Select at least one tract."),
            html.Div([dcc.Dropdown(id="tracts",
                    options=HEALTH_DATA.tract_code,
                    multi=True
                )
            ])
])

# -----------------------------------------
@app.callback(
            Output(component_id='health_output', component_property='children'),
            Input(component_id='health_inputs', component_property='value'),
            Input(component_id='tracts', component_property='value')
)
def update_health_output(health_metrics, tracts):
    if health_metrics:
        s = "summary score: {}".format(dc.create_summary_score(HEALTH_DATA, health_metrics, tracts))
        return s

if __name__ == '__main__':
    app.run_server(debug=True)