import pandas as pd
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from callbacks import get_data_table_filters_callbacks, get_data_table_entry_callbacks
from components import sidebar_component, navbar_component

# Load the data
url = "https://raw.githubusercontent.com/shoebjoarder/superstore/main/Sample%20-%20Superstore%20-%20CSV.csv"
df = pd.read_csv(url)
df = df.drop("Row ID", axis=1)
dff = df.copy(deep=True)

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    use_pages=True,
)


app.layout = dbc.Container(
    [
        dbc.Row([navbar_component()]),
        dbc.Row(
            [
                dbc.Col([sidebar_component()], lg=2),
                dbc.Col([dash.page_container], lg=10),
            ]
        ),
    ],
    fluid=True,
)

# Callbacks
get_data_table_filters_callbacks(app)
get_data_table_entry_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
