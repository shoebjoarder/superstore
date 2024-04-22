import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from datetime import date


def create_data_table_filters(df):
    accordion = [
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P("Apply filters to the Superstore data table below"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(["Segment"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-segment",
                                                    style={"margin-bottom": "16px"},
                                                ),
                                                html.Div(["Shop Mode"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-ship-mode",
                                                    style={"margin-bottom": "16px"},
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    ["Ship Date"],
                                                    style={"margin-bottom": "4px"},
                                                ),
                                                dcc.DatePickerRange(
                                                    id="ship-date-range",
                                                    min_date_allowed=date(1995, 8, 5),
                                                    max_date_allowed=date(2017, 9, 19),
                                                    initial_visible_month=date(
                                                        2017, 8, 5
                                                    ),
                                                    end_date=date(2017, 8, 25),
                                                ),
                                            ],
                                            style={
                                                "margin-bottom": "8px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    ["Order Date"],
                                                    style={"margin-bottom": "4px"},
                                                ),
                                                dcc.DatePickerRange(
                                                    id="order-date-range",
                                                    min_date_allowed=date(1995, 8, 5),
                                                    max_date_allowed=date(2017, 9, 19),
                                                    initial_visible_month=date(
                                                        2017, 8, 5
                                                    ),
                                                    end_date=date(2017, 8, 25),
                                                    style={"width": "100%"},
                                                ),
                                            ],
                                            style={
                                                "margin-bottom": "8px",
                                            },
                                        ),
                                    ],
                                    xs=12,
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(["Category"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-category",
                                                    style={"margin-bottom": "8px"},
                                                ),
                                                html.Div(["Sub-Category"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-sub-category",
                                                    style={"margin-bottom": "8px"},
                                                ),
                                            ],
                                            style={
                                                "border": "solid 1px #CFCFCF",
                                                "border-radius": "8px",
                                                "padding": "8px",
                                                "margin-bottom": "16px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(["Country"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-country",
                                                    style={"margin-bottom": "8px"},
                                                ),
                                                html.Div(["State"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-state",
                                                    style={"margin-bottom": "8px"},
                                                ),
                                                html.Div(["City"]),
                                                dcc.Dropdown(
                                                    [
                                                        "Item 1",
                                                        "Item 2",
                                                        "Item 3",
                                                    ],
                                                    "Item 1",
                                                    id="dropdown-city",
                                                    style={"margin-bottom": "8px"},
                                                ),
                                            ],
                                            style={
                                                "border": "solid 1px #CFCFCF",
                                                "border-radius": "8px",
                                                "padding": "8px",
                                            },
                                        ),
                                    ],
                                    xs=12,
                                    md=6,
                                ),
                            ],
                            className="g-3",
                        ),
                    ],
                    title="Filters",
                    style={"margin-bottom": "16px"},
                ),
            ],
            start_collapsed="True",
        ),
        "Allan",
    ]

    return accordion
