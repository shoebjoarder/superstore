import dash_bootstrap_components as dbc
import dash
from dash import dcc, dash_table, html
from .data_table_filters import create_data_table_filters
from .data_table_entry import create_data_table_entry


def create_layout() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                [
                    html.H4("Data Table"),
                    html.P("Preview and manipulate the Superstore data table below."),
                ],
                className="mt-4",
            ),
            dbc.Row([create_data_table_filters()]),
            dbc.Row(
                [
                    dcc.Loading(
                        [
                            dash_table.DataTable(
                                id="data-table",
                                page_size=10,
                                style_table={
                                    "maxWidth": "100%",
                                    "overflowX": "auto",
                                },
                                fill_width=True,
                            ),
                        ],
                        type="circle",
                    ),
                ],
                style={"min-height": "5vh"},
            ),
            dbc.Row([create_data_table_entry()], class_name="pt-3"),
        ]
    )


layout = create_layout()

dash.register_page(__name__, name="Data Table", path="/table-page")
