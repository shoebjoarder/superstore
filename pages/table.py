import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from dash import dcc, dash_table


def table_page(df):
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
                ], style={"margin-top": "32px", "margin-bottom": "16px"}
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1("Superstore Data Table"),
                            html.P(
                                "Preview and manipulate the Superstore data table below."
                            ),
                            dash_table.DataTable(
                                data=df.to_dict("records"),
                                page_size=10,
                                style_table={"maxWidth": "100%", "overflowX": "auto"},
                                fill_width=True,
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
