import pandas as pd
import dash
import dash_bootstrap_components as dbc
from callbacks import get_data_table_filters_callbacks, get_data_table_entry_callbacks
from components import sidebar_component, navbar_component
from utils import load_dataset


merged_df, df_original, df_table = load_dataset()


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
get_data_table_filters_callbacks(app, df_table)
get_data_table_entry_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
