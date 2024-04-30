import dash_bootstrap_components as dbc
import dash
from dash import dash_table, html
from .data_table_filters import create_data_table_filters
from .data_table_entry import create_data_table_entry


def create_layout() -> dbc.Container:
    return dbc.Container(
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
            dbc.Row([create_data_table_entry()]),
        ]
    )


layout = create_layout()

dash.register_page(__name__, name="Data Table", path="/table-page")
