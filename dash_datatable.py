from dash import Dash, dash_table
import pandas as pd
from functools import reduce
import data_cleaning as dc

# Importing all dfs
df = dc.tract_to_neighborhood()

app = Dash(__name__)

app.layout = dash_table.DataTable(
    data=df.to_dict('records'), 
    columns=[{"name": i, "id": i} for i in df.columns],
    style_cell={'fontSize':20, 'font-family':'sans-serif', 'padding': '5px'},
    style_header={'fontWeight': 'bold'},)


if __name__ == '__main__':
    app.run_server(debug=True)