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
                                                        sorted(df["Segment"].unique()),
                                                        id="dropdown-segment",
                                                        className="mb-3",
                                                    ),
                                                    html.Div(["Ship Mode"]),
                                                    dcc.Dropdown(
                                                        sorted(
                                                            df["Ship Mode"].unique()
                                                        ),
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
                                                                        max_date_allowed=df[
                                                                            "Ship Date"
                                                                        ].max(),
                                                                        initial_visible_month=df[
                                                                            "Ship Date"
                                                                        ].max(),
                                                                        clearable=True,
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
                                                                # xl=6,
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
                                                                        max_date_allowed=df[
                                                                            "Order Date"
                                                                        ].max(),
                                                                        initial_visible_month=df[
                                                                            "Order Date"
                                                                        ].max(),
                                                                        style={
                                                                            "width": "100%"
                                                                        },
                                                                        clearable=True,
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                                xs=12,
                                                                # xl=6,
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
                                                        sorted(df["Category"].unique()),
                                                        id="dropdown-category",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["Sub-Category"]),
                                                    dcc.Dropdown(
                                                        sorted(
                                                            df["Sub-Category"].unique()
                                                        ),
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
                                                        sorted(df["Country"].unique()),
                                                        id="dropdown-country",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["State"]),
                                                    dcc.Dropdown(
                                                        sorted(df["State"].unique()),
                                                        id="dropdown-state",
                                                        className="mb-2",
                                                    ),
                                                    html.Div(["City"]),
                                                    dcc.Dropdown(
                                                        sorted(df["City"].unique()),
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
                                                        className="bi bi-list-nested"
                                                    ),
                                                    " Clear all",
                                                ],
                                                color="primary",
                                                id="clear-filter",
                                                disabled=True,
                                                outline=True,
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
                                                n_clicks=0,
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
        # start_collapsed="True",
    )

    return accordion
