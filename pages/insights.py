import dash_bootstrap_components as dbc
import dash
from dash import dcc, html

dash.register_page(__name__, name="Insights", path="/graph-page")


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Insights"),
                        html.P(
                            "Interactive charts that provides in-depth insights for your analysis."
                        ),
                    ]
                ),
            ],
            className="mt-4 mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(["Select data"]),
                        dcc.Dropdown(
                            value="Discount",
                            id="dropdown-timeline-graph",
                            clearable=False,
                        ),
                        dcc.Graph(id="insights-timeline-graph"),
                    ],
                    xs=12,
                    xl=6,
                    className="mb-5",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(["X-Axis"]),
                                        dcc.Dropdown(
                                            value="Discount",
                                            id="dropdown-scatter-x-axis",
                                            placeholder="Select x-axis",
                                            clearable=False,
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(["Y-Axis"]),
                                        dcc.Dropdown(
                                            value="Profit",
                                            id="dropdown-scatter-y-axis",
                                            placeholder="Select y-axis",
                                            clearable=False,
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(["Select data"]),
                                        dcc.Dropdown(
                                            value="Segment",
                                            id="dropdown-scatter-categorical",
                                            placeholder="Select categorical data",
                                            clearable=False,
                                        ),
                                    ],
                                    xs=4,
                                ),
                            ]
                        ),
                        dcc.Graph(id="insights-scatterplot-graph"),
                    ],
                    xs=12,
                    xl=6,
                    className="mb-5",
                ),
            ],
        ),
    ]
)
