import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from datetime import date


def create_data_table_entry(df):
    accordion = [
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Container(  # Using dbc.Container to better manage the alignment and padding
                            dbc.Row(
                                [
                                    html.P("Fill out the form below to add a new data"),
                                    dbc.Col(
                                        [
                                            html.Div(["Order ID"]),
                                            dbc.Input(
                                                id="order-id",
                                                placeholder="Enter order ID",
                                                type="text",
                                            ),
                                        ],
                                        width=12,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(["Order date"]),
                                            dcc.DatePickerSingle(
                                                id="date-picker",
                                                min_date_allowed=date(1995, 8, 5),
                                                max_date_allowed=date(2017, 9, 19),
                                                initial_visible_month=date(2017, 8, 5),
                                                date=date(2017, 8, 25),
                                            ),
                                        ],
                                        width=12,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(["Customer ID"]),
                                            dbc.Input(
                                                id="customer-id",
                                                placeholder="Enter customer ID",
                                                type="text",
                                            ),
                                        ],
                                        width=12,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(["Product ID"]),
                                            dbc.Input(
                                                id="product-id",
                                                placeholder="Enter product ID",
                                                type="text",
                                            ),
                                        ],
                                        width=12,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(["Quantity"]),
                                            dbc.Input(
                                                id="quantity",
                                                placeholder="Enter quantity",
                                                type="text",
                                            ),
                                        ],
                                        width=12,
                                        className="mb-4",
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-floppy"
                                                    ),
                                                    " Add to data table"
                                                ],
                                                color="primary",
                                            ),
                                        ],
                                        width=12,
                                        className="mb-3 d-grid gap-2",
                                    ),
                                ],
                                justify="center",  # Center align items horizontally
                                style={
                                    "max-width": "600px",
                                    "margin": "0 auto",
                                },  # Center align the row
                            ),
                            fluid=True,
                        ),
                    ],
                    title="Do you want to add a new entry to the table?",
                    className="mb-3",
                ),
            ],
            # start_collapsed="True",
        ),
        "Allan",
    ]

    return accordion
