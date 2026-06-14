import logging
import dash
import dash_bootstrap_components as dbc
import callbacks
import components
from dash import dcc, Input, Output, State
from utils import load_dataset
import os
from dotenv import load_dotenv

load_dotenv()

dataset_url = os.getenv("DATASET_URL")

# Configuration of logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load the dataset
dataset_df = load_dataset(url=dataset_url)

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    use_pages=True,
    # Callbacks reference components that live on pages other than the one
    # currently rendered (the filter/data-entry controls). This is the standard
    # setting for multi-page apps and silences benign "nonexistent object"
    # warnings when a shared store updates while another page is shown.
    suppress_callback_exceptions=True,
)
server = app.server

# Initialize the layout
app.layout = dbc.Container(
    [
        # The dataset is embedded only once (here). "memory-original" is mirrored
        # from it in the browser by a clientside callback at load, and
        # "memory-filter" is a scratch buffer that starts empty. This keeps the
        # initial page payload at ~1 copy of the data instead of three.
        dcc.Store(id="memory-table", data=dataset_df.to_dict("records")),
        dcc.Store(id="memory-original", data=[]),
        dcc.Store(id="memory-filter", data=[]),
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

# Mirror the dataset into "memory-original" once, in the browser, without
# re-downloading it. Guarded on the current value so later updates to
# "memory-table" (filtering, data entry) never clobber the pristine original.
app.clientside_callback(
    """
    function(tableData, originalData) {
        if (originalData && originalData.length > 0) {
            return window.dash_clientside.no_update;
        }
        return tableData;
    }
    """,
    Output("memory-original", "data"),
    Input("memory-table", "data"),
    State("memory-original", "data"),
)

# Callbacks
callbacks.data_table_filters_callbacks(app)
callbacks.data_table_entry_callbacks(app)
callbacks.data_table_callbacks(app)
callbacks.insights_callbacks(app)
callbacks.dashboard_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
