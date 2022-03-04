from dash import Dash, dash_table
import pandas as pd

VAR_NAMES = {"GEOID":"Tract Code",
            "HDX_2015-2019":"Hardship Score"}

def rename_cols(filename):
    df = pd.read_csv(filename)
    cols_to_keep = list(VAR_NAMES.keys())
    df = df[cols_to_keep]
    final_df = df.rename(columns=VAR_NAMES)
    return final_df

df = rename_cols('hardship_index.csv')

app = Dash(__name__)

app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


if __name__ == '__main__':
    app.run_server(debug=True)