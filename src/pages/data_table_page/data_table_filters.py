import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import date


def create_data_table_filters():
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
                                                        options=[],
                                                        id="dropdown-segment",
                                                        className="mb-3",
                                                    ),
                                                    html.Div(["Ship Mode"]),
                                                    dcc.Dropdown(
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
                                                                        clearable=True,
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
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
                                                                        style={
                                                                            "width": "100%"
                                                                        },
                                                                        clearable=True,
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
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
                                                        id="dropdown-category",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["Sub-Category"]),
                                                    dcc.Dropdown(
                                                        id="dropdown-sub-category",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                style={
                                                    "border": "solid 1px #CFCFCF",
                                                    "borderRadius": "8px",
                                                    "padding": "8px",
                                                    "marginBottom": "16px",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(["Country"]),
                                                    dcc.Dropdown(
                                                        id="dropdown-country",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["State"]),
                                                    dcc.Dropdown(
                                                        id="dropdown-state",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["City"]),
                                                    dcc.Dropdown(
                                                        id="dropdown-city",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                style={
                                                    "border": "solid 1px #CFCFCF",
                                                    "borderRadius": "8px",
                                                    "padding": "8px",
                                                },
                                            ),
                                        ],
                                        xs=12,
                                        md=6,
                                    ),
                                ],
                                className="g-3 mb-3",
                            ),
                            dbc.Row([html.Hr()]),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="fa-solid fa-broom"
                                                    ),
                                                    " Clear all",
                                                ],
                                                color="primary",
                                                id="clear-filter",
                                                disabled=True,
                                            ),
                                        ],
                                        className="d-flex justify-content-start",
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                children=["Apply Filters"],
                                                color="primary",
                                                id="submit-filter",
                                            ),
                                        ],
                                        className="d-flex justify-content-end",
                                    ),
                                ],
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
