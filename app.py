import pandas as pd
import dash
import dash_bootstrap_components as dbc
import callbacks
import components
from dash import dcc
from utils import load_dataset


df_original, df_table = load_dataset()


# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.MATERIA,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
    use_pages=True,
)


app.layout = dbc.Container(
    [
        dcc.Store(id="memory-output", data=df_table.to_dict("records")),
        dbc.Row([components.navbar_component()]),
        dbc.Row(
            [
                dbc.Col([components.sidebar_component()], lg=2),
                dbc.Col([dash.page_container], lg=10),
            ]
        ),
    ],
    fluid=True,
)

# Callbacks
callbacks.data_table_filters_callbacks(app)
callbacks.data_table_entry_callbacks(app)
callbacks.data_table_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
