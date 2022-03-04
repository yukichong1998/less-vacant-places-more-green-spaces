from dash import Dash, dcc, html, Input, Output
import data_cleaning as dc

#load data
HEALTH_COLS = ["stcotr_fips", "est"]

physical_distress = dc.load_health_data("health_physical_distress.csv", HEALTH_COLS, "Physical Distress")
mental_distress = dc.load_health_data("health_mental_distress.csv", HEALTH_COLS, "Mental Distress")
diabetes = dc.load_health_data("health_diabetes.csv", HEALTH_COLS, "Diabetes")
hbp = dc.load_health_data("health_high_blood_pressure.csv", HEALTH_COLS, "High Blood Pressure")
life_expectancy = dc.load_health_data("health_life_expectancy.csv", HEALTH_COLS, "Life Expectancy")

HEALTH_DATA = physical_distress.merge(mental_distress).merge(diabetes).merge(hbp).merge(life_expectancy)
HEALTH_DATA = HEALTH_DATA.astype({"census_tract": str})

app = Dash(__name__)

app.layout = html.Div([
            html.H6("Select at least one health indicator."),
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
                            }
                )
            ])
        ])
])

# -----------------------------------------
@app.callback(
            Output(component_id='health_output', component_property='children'),
            Input(component_id='health_inputs', component_property='value'),
            Input(component_id='tracts', component_property='value'),
            Input(component_id='health_inputs_checklist', component_property='value')
)
def update_health_output(health_metrics, tracts):
    if health_metrics:
        s = "summary score: {}".format(dc.create_summary_score(HEALTH_DATA, health_metrics, tracts))
        return s

if __name__ == '__main__':
    app.run_server(debug=True)