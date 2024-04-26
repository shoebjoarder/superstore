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
                        dcc.Dropdown(
                            [
                                "Discount",
                                "Profit",
                                "Profit Ratio",
                                "Quantity",
                                "Returned",
                                "Sales",
                            ],
                            value="Discount",
                            id="dropdown-timeline-graph",
                        ),
                        dcc.Graph(id="insights-timeline-graph"),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-5",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Days to Ship",
                                                "Discount",
                                                "Profit",
                                                "Profit Ratio",
                                                "Quantity",
                                                "Returns",
                                                "Sales",
                                            ],
                                            id="dropdown-x-axis",
                                            placeholder="Select x-axis",
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Discount",
                                                "Profit",
                                                "Profit Ratio",
                                                "Quantity",
                                                "Returns",
                                                "Sales",
                                            ],
                                            id="dropdown-y-axis",
                                            placeholder="Select y-axis",
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Segment",
                                                "Ship Mode",
                                                "Customer Name",
                                                "Category",
                                                "Sub-Category",
                                                "Product Name",
                                            ],
                                            id="dropdown-breakdown",
                                            placeholder="Select categorical data",
                                        ),
                                    ],
                                    xs=4,
                                ),
                            ]
                        ),
                        # dcc.Graph(id="graph-scatterplot", figure=plot_fig),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-5",
                ),
            ],
        ),
    ]
)
