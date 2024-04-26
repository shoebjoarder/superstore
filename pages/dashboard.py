import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from dash import dcc, html
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import df_original as dff

dash.register_page(__name__, name="Dashboard", path="/")

dff["Order Date"] = pd.to_datetime(dff["Order Date"])

# Calculate most_recent_date and four_months_ago as Timestamp objects
most_recent_date = dff["Order Date"].max()
four_months_ago = most_recent_date - pd.Timedelta(days=120)

# Now, the comparison should work without errors
recent_data = dff[
    (dff["Order Date"] >= four_months_ago) & (dff["Order Date"] <= most_recent_date)
]

# # Filter dff for the last four months
# most_recent_date = pd.to_datetime(dff["Order Date"].max())
# four_months_ago = most_recent_date - pd.Timedelta(days=120)

# # Filter dff for the previous four months
# recent_data = dff[
#     (dff["Order Date"] >= four_months_ago) & (dff["Order Date"] <= most_recent_date)
# ]

# Calculate accumulated sales and profit ratio
accumulated_sales = recent_data["Sales"].sum()
profit_ratio = dff["Profit"].sum() / accumulated_sales

# Group by 'Month', then sum 'Sales' for each unique year-month combination
grouped_sales_monthly = (
    recent_data.resample("ME", on="Order Date")["Sales"].sum().reset_index()
)
grouped_profit_monthly = (
    recent_data.resample("ME", on="Order Date")["Profit"].sum().reset_index()
)

# Group by 'Order Date' and sum 'Sales' for each unique date
# grouped_sales = recent_data.groupby("Order Date")["Sales"].sum().reset_index()
# grouped_profit = recent_data.groupby("Order Date")["Profit"].sum().reset_index()

# Rename the columns for clarity
# grouped_sales.columns = ["Order Date", "Total Sales"]
# grouped_profit.columns = ["Order Date", "Total Profit"]

# Rename the columns for clarity
grouped_sales_monthly.columns = ["Order Date", "Total Sales"]
grouped_profit_monthly.columns = ["Order Date", "Total Profit"]

# Create a line chart for sales and profit
sales_fig = px.line(
    grouped_sales_monthly, x="Order Date", y="Total Sales", title="Sales Trends"
)
profit_fig = px.line(
    grouped_profit_monthly, x="Order Date", y="Total Profit", title="Profit Trends"
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Superstore Dashboard"),
                        html.P(
                            "An overview of the most recent data of the Superstore."
                        ),
                    ]
                ),
            ],
            className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.P(
                                                        "Accumulated Sales",
                                                        className="card-title",
                                                    ),
                                                    style={"flex": "1"},
                                                ),
                                                dbc.Col(
                                                    html.I(
                                                        className="bi bi-info-circle",
                                                        id="tooltip-target-acc-sales",
                                                    ),
                                                    style={
                                                        "flex": "0",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                                dbc.Tooltip(
                                                    "The number represents the accumulated sales in the past four months.",
                                                    target="tooltip-target-acc-sales",
                                                ),
                                            ],
                                        ),
                                        html.H4(
                                            f"${accumulated_sales:,.2f}",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.P(
                                                        "Profit Ratio",
                                                        className="card-title",
                                                    ),
                                                    style={"flex": "1"},
                                                ),
                                                dbc.Col(
                                                    html.I(
                                                        className="bi bi-info-circle",
                                                        id="tooltip-target-profit-ratio",
                                                    ),
                                                    style={
                                                        "flex": "0",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                                dbc.Tooltip(
                                                    "The number represents the profit ratio in the past four months.",
                                                    target="tooltip-target-profit-ratio",
                                                ),
                                            ],
                                        ),
                                        html.H4(
                                            f"{profit_ratio:.2%}",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="sales-graph", figure=sales_fig),
                    ],
                    className="mb-3",
                    xs=12,
                    lg=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="profit-graph", figure=profit_fig),
                    ],
                    className="mb-3",
                    xs=12,
                    lg=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Superstore Data Table",
                                            className="card-title",
                                        ),
                                        html.P(
                                            "Preview and manipulate the Superstore data table.",
                                            className="card-text",
                                        ),
                                        dbc.Button(
                                            [
                                                "To data table ",
                                                html.I(
                                                    className="fa-solid fa-arrow-right"
                                                ),
                                            ],
                                            color="primary",
                                            href="/table-page",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Superstore Insights",
                                            className="card-title",
                                        ),
                                        html.P(
                                            "Get insights into the data using interactive charts.",
                                            className="card-text",
                                        ),
                                        dbc.Button(
                                            [
                                                "To insights ",
                                                html.I(
                                                    className="fa-solid fa-arrow-right"
                                                ),
                                            ],
                                            color="primary",
                                            href="/graph-page",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="mb-3",
                    xs=12,
                    md=6,
                ),
            ]
        ),
    ]
)
