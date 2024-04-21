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
                        html.P("Fill out the form below to add a new data"),
                    ],
                    title="Do you want to add a new entry to the table?",
                    style={"margin-bottom": "16px"},
                ),
            ],
            # start_collapsed="True",
        ),
        "Allan",
    ]

    return accordion
