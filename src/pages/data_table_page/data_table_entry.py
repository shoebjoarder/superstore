import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import date
from typing import Any, List


def create_input(title: str, type: str) -> List[Any]:
    title_hypen = title.lower().replace(" ", "-")
    return [
        dbc.Label(title),
        dbc.Input(
            id=f"input-{title_hypen}",
            type=type,
        ),
    ]


def create_data_table_entry() -> dbc.Accordion:
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Container(
                        [
                            dbc.Container(
                                [
                                    dbc.Label(["Fill out the form below to add a new data"], class_name="pb-3"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Label("Order date"),
                                                    dcc.DatePickerSingle(
                                                        id="input-order-date",
                                                        max_date_allowed=date.today(),
                                                        initial_visible_month=date.today(),
                                                        date=date.today(),
                                                    ),
                                                ],
                                                className="mb-3",
                                                xs=12,
                                                md=3,
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Label("Ship Mode"),
                                                    dbc.Select(
                                                        options=[],
                                                        id="input-ship-mode",
                                                        value=None,
                                                        # searchable=False,
                                                        className="mb-2",
                                                    ),
                                                ],
                                                xs=12,
                                                md=9,
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                ]
                            ),
                            dbc.Container(
                                create_input("Order ID", "text"),
                                className="mb-4",
                            ),
                            dbc.Container(
                                create_input("Customer ID", "text"),
                                className="mb-4",
                            ),
                            dbc.Container(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                create_input("Product ID", "text"),
                                                xs=8,
                                            ),
                                            dbc.Col(
                                                create_input("Quantity", "number"),
                                                className="mb-3",
                                                xs=4,
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-4",
                            ),
                            dbc.Container(
                                [
                                    dbc.Button(
                                        "Submit",
                                        id="submit-data-entry",
                                        color="primary",
                                        disabled=True,
                                    ),
                                ],
                                className="mb-3 d-grid",
                            ),
                        ],
                        style={
                            "maxWidth": "600px",
                            "margin": "0 auto",
                            "marginTop": "8px",
                        },
                        fluid=True,
                    ),
                ],
                title="Do you want to add a new data to the table? Click here.",
                className="mb-3",
            ),
            dbc.Toast(
                html.Div(id="data-entry-feedback"),
                id="data-entry-feedback-toast",
                header="Data added successfully",
                duration=7000,
                is_open=False,
                icon="success",
                style={
                    "position": "fixed",
                    "bottom": "20px",
                    "left": "24px",
                    "width": 350,
                },
            ),
        ],
        start_collapsed="True",
    )
