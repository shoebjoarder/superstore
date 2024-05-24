import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import date


def filter_dropdown(title: str) -> dbc.Row:
    title_hypen = title.lower().replace(" ", "-")
    return dbc.Row(
        [
            html.Div(
                [
                    dbc.Label(title),
                    dcc.Dropdown(
                        options=[],
                        id=f"dropdown-filter-{title_hypen}",
                        searchable=False,
                    ),
                ]
            )
        ],
        class_name="mb-3",
    )


def date_range(title: str) -> dbc.Row:
    title_hypen = title.lower().replace(" ", "-")
    return dbc.Row(
        [
            dbc.Label(title),
            html.Div(
                [
                    dcc.DatePickerRange(
                        id=f"filter-{title_hypen}-range",
                        min_date_allowed=date(
                            1995,
                            8,
                            5,
                        ),
                        display_format="YYYY-MM-DD",
                        clearable=True,
                        className="date-picker-range"
                    ),
                ],
            ),
        ],
        className="mb-3",
    )


def create_data_table_filters() -> dbc.Accordion:
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Container(
                        [
                            dbc.Label(
                                ["Apply filters to the Superstore data table below"],
                                class_name="pb-3",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            filter_dropdown("Segment"),
                                            filter_dropdown("Ship Mode"),
                                            date_range("Ship Date"),
                                            date_range("Order Date"),
                                        ],
                                        xs=12,
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Container(
                                                [
                                                    filter_dropdown("Category"),
                                                    filter_dropdown("Sub-Category"),
                                                ],
                                                style={
                                                    "border": "solid 1px #CFCFCF",
                                                    "borderRadius": "8px",
                                                    "padding": "8px",
                                                    "marginBottom": "16px",
                                                },
                                            ),
                                            dbc.Container(
                                                [
                                                    filter_dropdown("Country"),
                                                    filter_dropdown("State"),
                                                    filter_dropdown("City"),
                                                ],
                                                style={
                                                    "border": "solid 1px #CFCFCF",
                                                    "borderRadius": "8px",
                                                    "padding": "8px",
                                                    "marginBottom": "16px",
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
                                            )
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
