import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import date


def create_data_table_entry():
    accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Container(
                        dbc.Row(
                            [
                                html.P("Fill out the form below to add a new data"),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(["Order date"]),
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
                                                        html.Div(["Ship Mode"]),
                                                        dcc.Dropdown(
                                                            options=[],
                                                            id="input-ship-mode",
                                                            value=None,
                                                            className="mb-2",
                                                        ),
                                                    ],
                                                    xs=12,
                                                    md=9,
                                                ),
                                            ]
                                        ),
                                    ],
                                    xs=12,
                                    className="mb-3",
                                ),
                                dbc.Col(
                                    [
                                        html.Div(["Customer ID"]),
                                        dbc.Input(
                                            id="input-customer-id",
                                            placeholder="Enter customer ID",
                                            type="text",
                                        ),
                                    ],
                                    className="mb-3",
                                    xs=12,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(["Product ID"]),
                                                        dbc.Input(
                                                            id="input-product-id",
                                                            placeholder="Enter product ID",
                                                            type="text",
                                                        ),
                                                    ],
                                                    xs=8,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Div(["Quantity"]),
                                                        dbc.Input(
                                                            id="input-quantity",
                                                            placeholder="Enter number",
                                                            type="number",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                    xs=4,
                                                ),
                                            ]
                                        )
                                    ],
                                    width=12,
                                    className="mb-4",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Submit",
                                            id="submit-data-entry",
                                            color="primary",
                                            n_clicks=0,
                                            disabled=True,
                                        ),
                                    ],
                                    width=12,
                                    className="mb-3 d-grid gap-2",
                                ),
                            ],
                            justify="center",
                            style={
                                "max-width": "600px",
                                "margin": "0 auto",
                            },
                        ),
                        fluid=True,
                    ),
                ],
                title="Do you want to add a new entry to the data table? Click here.",
                className="mb-3",
            ),
            dbc.Toast(
                html.Div(
                    id="container-button-basic",
                ),
                id="positioned-toast",
                header="Data added successfully",
                duration=4000,
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

    return accordion
