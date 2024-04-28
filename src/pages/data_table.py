import dash_bootstrap_components as dbc
import dash
from dash import dash_table, html
from .page_components import *


dash.register_page(__name__, name="Data Table", path="/table-page")

data_table_entry = create_data_table_entry()

layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H4("Data Table"),
                html.P("Preview and manipulate the Superstore data table below."),
                # Filter from the filter component for the data table
                create_data_table_filters(),
                dash_table.DataTable(
                    id="data-table",
                    page_size=10,
                    style_table={"maxWidth": "100%", "overflowX": "auto"},
                    fill_width=True,
                ),
            ],
            className="pb-3 mt-4",
        ),
        dbc.Row([data_table_entry]),
    ]
)
