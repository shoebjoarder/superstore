import dash
import dash_bootstrap_components as dbc
import callbacks
import app_components
from dash import dcc
from utils import load_dataset
import os
from dotenv import load_dotenv

load_dotenv()

dataset_url = os.getenv("DATASET_URL")

# Load the dataset
df_table = load_dataset(url=dataset_url)

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
server = app.server

# Initialize the layout
app.layout = dbc.Container(
    [
        dcc.Store(id="memory-output", data=df_table.to_dict("records")),
        dbc.Row([app_components.navbar_component()]),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [app_components.sidebar_component()],
                            xl=2,
                        ),
                        dbc.Col(
                            [dash.page_container],
                            xl=10,
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
)

# Callbacks
callbacks.data_table_filters_callbacks(app)
callbacks.data_table_entry_callbacks(app)
callbacks.data_table_callbacks(app)
callbacks.insights_callbacks(app)
callbacks.dashboard_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)