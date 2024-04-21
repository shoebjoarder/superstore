import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, dash_table
from datetime import date
from .page_components import create_data_table_filters, create_data_table_entry


def table_page(df):
    [filters, string] = create_data_table_filters(df)
    [add_new_data, string] = create_data_table_entry(df)
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                [html.I(className="bi bi-arrow-left"), " Back"],
                                color="light",
                                href="/",
                                className="me-1",
                            ),
                        ]
                    ),
                ],
                style={"margin-top": "32px", "margin-bottom": "16px"},
            ),
            dbc.Row(
                [
                    html.H2("Superstore Data Table"),
                    html.P("Preview and manipulate the Superstore data table below."),
                    # Filter from the filter component for the data table
                    filters,
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        page_size=10,
                        style_table={"maxWidth": "100%", "overflowX": "auto"},
                        fill_width=True,
                    ),
                ],
                style={"padding-bottom": "16px"}
            ),
            dbc.Row([
                add_new_data,
            ])
        ]
    )
