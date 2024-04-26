import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, dash_table
from datetime import date
# from .page_components import create_data_table_filters, create_data_table_entry
from .page_components import *
from app import df_table as df
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

dash.register_page(__name__, name="Data Table", path="/table-page")


filters = create_data_table_filters(df)
add_new_data = create_data_table_entry()

layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H2("Data Table"),
                html.P("Preview and manipulate the Superstore data table below."),
                # Filter from the filter component for the data table
                filters,
                dash_table.DataTable(
                    id="data-table",
                    page_size=15,
                    style_table={"maxWidth": "100%", "overflowX": "auto"},
                    fill_width=True,
                ),
            ],
            className="pb-3 mt-4",
        ),
        dbc.Row([add_new_data]),
    ]
)
