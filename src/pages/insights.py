import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
from datetime import date

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
                html.Div(["Filter by date"]),
                dcc.DatePickerRange(
                    id="insights-date-range",
                    # TODO: FIX required to help choose date easily
                    min_date_allowed=date(
                        1995,
                        8,
                        5,
                    ),
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    clearable=True,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
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
                                    ],
                                    xs=6,
                                    className="mb-2",
                                ),
                                dbc.Col(
                                    [
                                        html.Div(["Select Week/Month/Quarter/Year"]),
                                        dcc.Dropdown(
                                            # ["Week", "Month", "Quarter", "Year"],
                                            value="Month",
                                            id="dropdown-week-month-quarter-year",
                                            clearable=False,
                                        ),
                                    ],
                                    xs=6,
                                    className="mb-2",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dcc.Graph(id="insights-timeline-graph"),
                            ]
                        ),
                    ],
                    xs=12,
                    # xl=6,
                    className="mb-5",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
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
                    # xl=6,
                    className="mb-5",
                ),
            ],
        ),
    ]
)
