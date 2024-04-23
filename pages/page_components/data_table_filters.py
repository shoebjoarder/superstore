import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from datetime import date


def create_data_table_filters(df):
    accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("Apply filters to the Superstore data table below"),
                    dbc.Container(
                        [
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
                                                        id="dropdown-segment",
                                                        className="mb-3",
                                                    ),
                                                    # TODO: Testing callback, remove later
                                                    html.Div(id="dd-output-container"),
                                                    # 
                                                    html.Div(["Shop Mode"]),
                                                    dcc.Dropdown(
                                                        [
                                                            "Item 1",
                                                            "Item 2",
                                                            "Item 3",
                                                        ],
                                                        id="dropdown-ship-mode",
                                                        className="mb-3",
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        ["Ship Date"]
                                                                    ),
                                                                    dcc.DatePickerRange(
                                                                        id="ship-date-range",
                                                                        min_date_allowed=date(
                                                                            1995,
                                                                            8,
                                                                            5,
                                                                        ),
                                                                        max_date_allowed=date(
                                                                            2017,
                                                                            9,
                                                                            19,
                                                                        ),
                                                                        initial_visible_month=date(
                                                                            2017,
                                                                            8,
                                                                            5,
                                                                        ),
                                                                        end_date=date(
                                                                            2017,
                                                                            8,
                                                                            25,
                                                                        ),
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
                                                                xl=6,
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        ["Order Date"]
                                                                    ),
                                                                    dcc.DatePickerRange(
                                                                        id="order-date-range",
                                                                        min_date_allowed=date(
                                                                            1995,
                                                                            8,
                                                                            5,
                                                                        ),
                                                                        max_date_allowed=date(
                                                                            2017,
                                                                            9,
                                                                            19,
                                                                        ),
                                                                        initial_visible_month=date(
                                                                            2017,
                                                                            8,
                                                                            5,
                                                                        ),
                                                                        end_date=date(
                                                                            2017,
                                                                            8,
                                                                            25,
                                                                        ),
                                                                        style={
                                                                            "width": "100%"
                                                                        },
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
                                                                xl=6,
                                                            ),
                                                        ]
                                                    )
                                                ],
                                                className="mb-2",
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
                                                        id="dropdown-category",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["Sub-Category"]),
                                                    dcc.Dropdown(
                                                        [
                                                            "Item 1",
                                                            "Item 2",
                                                            "Item 3",
                                                        ],
                                                        id="dropdown-sub-category",
                                                        className="mb-2",
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
                                                        id="dropdown-country",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["State"]),
                                                    dcc.Dropdown(
                                                        [
                                                            "Item 1",
                                                            "Item 2",
                                                            "Item 3",
                                                        ],
                                                        id="dropdown-state",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["City"]),
                                                    dcc.Dropdown(
                                                        [
                                                            "Item 1",
                                                            "Item 2",
                                                            "Item 3",
                                                        ],
                                                        id="dropdown-city",
                                                        className="mb-2",
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
                        ]
                    ),
                ],
                title="Filters",
                className="mb-3",
            ),
        ],
        start_collapsed="True",
    )

    return accordion
