import logging
import dash
import dash_bootstrap_components as dbc
import callbacks
import components
from dash import dcc
from utils import load_dataset
import os
from dotenv import load_dotenv

load_dotenv()

dataset_url = os.getenv("DATASET_URL")

# Configuration of logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load the dataset
df_table = load_dataset(url=dataset_url)

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LITERA, dbc.icons.FONT_AWESOME],
    use_pages=True,
)
server = app.server

# Initialize the layout
app.layout = dbc.Container(
    [
        dcc.Store(id="memory-table", data=df_table.to_dict("records")),
        dcc.Store(id="memory-original", data=df_table.to_dict("records")),
        dcc.Store(id="memory-filter", data=df_table.to_dict("records")),
        dbc.Row([components.navbar_component()]),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [components.sidebar_component()],
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
