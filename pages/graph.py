import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html


def graph_page():
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
                    dbc.Col(
                        [
                            html.H1("Graph Page"),
                            # dcc.Graph(id="graph-graph", figure=profit_fig),
                        ]
                    ),
                ]
            ),
        ]
    )
