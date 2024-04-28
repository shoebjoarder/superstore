import dash_bootstrap_components as dbc
import dash
from dash import dcc, html

dash.register_page(__name__, name="Dashboard", path="/")


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Superstore Dashboard"),
                        html.P(
                            "An overview of the most recent data of the Superstore."
                        ),
                    ]
                ),
            ],
            className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.P(
                                                        "Accumulated Sales",
                                                        className="card-title",
                                                    ),
                                                    style={"flex": "1"},
                                                ),
                                                dbc.Col(
                                                    html.I(
                                                        className="fa-regular fa-circle-question",
                                                        id="tooltip-target-acc-sales",
                                                    ),
                                                    style={
                                                        "flex": "0",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                                dbc.Tooltip(
                                                    "The number represents the accumulated sales in the past 12 months.",
                                                    target="tooltip-target-acc-sales",
                                                ),
                                            ],
                                        ),
                                        html.H4(
                                            id="accumulated-sales",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.P(
                                                        "Profit Ratio",
                                                        className="card-title",
                                                    ),
                                                    style={"flex": "1"},
                                                ),
                                                dbc.Col(
                                                    html.I(
                                                        className="fa-regular fa-circle-question",
                                                        id="tooltip-target-profit-ratio",
                                                    ),
                                                    style={
                                                        "flex": "0",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                                dbc.Tooltip(
                                                    "The number represents the profit ratio in the past 12 months.",
                                                    target="tooltip-target-profit-ratio",
                                                ),
                                            ],
                                        ),
                                        html.H4(
                                            id="profit-ratio",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [dcc.Graph(id="dashboard-sales-graph")],
                    className="mb-3",
                    xs=12,
                    lg=6,
                ),
                dbc.Col(
                    [dcc.Graph(id="dashboard-profit-graph")],
                    className="mb-3",
                    xs=12,
                    lg=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Superstore Data Table",
                                            className="card-title",
                                        ),
                                        html.P(
                                            "Preview and manipulate the Superstore data table.",
                                            className="card-text",
                                        ),
                                        dbc.Button(
                                            [
                                                "To data table ",
                                                html.I(
                                                    className="fa-solid fa-arrow-right"
                                                ),
                                            ],
                                            color="primary",
                                            href="/table-page",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Superstore Insights",
                                            className="card-title",
                                        ),
                                        html.P(
                                            "Get insights into the data using interactive charts.",
                                            className="card-text",
                                        ),
                                        dbc.Button(
                                            [
                                                "To insights ",
                                                html.I(
                                                    className="fa-solid fa-arrow-right"
                                                ),
                                            ],
                                            color="primary",
                                            href="/graph-page",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
            ]
        ),
    ]
)
