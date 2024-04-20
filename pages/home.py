import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from dash import dcc


def home_page(df):
    # Convert 'Order Date' to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Filter df for the last four months
    most_recent_date = df["Order Date"].max()
    four_months_ago = most_recent_date - pd.Timedelta(days=120)

    # Filter df for the previous four months
    recent_data = df[
        (df["Order Date"] >= four_months_ago) & (df["Order Date"] <= most_recent_date)
    ]

    # Calculate accumulated sales and profit ratio
    accumulated_sales = recent_data["Sales"].sum()
    profit_ratio = df["Profit"].sum() / accumulated_sales

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
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1("Superstore Dashboard"),
                            html.P(
                                "An overview of the most recent data of the Superstore."
                            ),
                        ]
                    ),
                ],
                style={"margin-top": "32px"},
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
                                                        html.H5(
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
                                                        "The number represents the accumulated sales of the past four months.",
                                                        target="tooltip-target-acc-sales",
                                                    ),
                                                ],
                                            ),
                                            html.P(
                                                f"${accumulated_sales:,.2f}",
                                                className="card-text",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
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
                                                        html.H5(
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
                                                        "The number represents the profit ratio of the past four months.",
                                                        target="tooltip-target-profit-ratio",
                                                    ),
                                                ],
                                            ),
                                            html.P(
                                                f"{profit_ratio:.2%}",
                                                className="card-text",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id="sales-graph", figure=sales_fig),
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id="profit-graph", figure=profit_fig),
                        ]
                    ),
                ]
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
                                                "Here you can preview and manipulate the Superstore data table.",
                                                className="card-text",
                                            ),
                                            dbc.Button(
                                                [
                                                    "To table ",
                                                    html.I(
                                                        className="bi bi-arrow-right"
                                                    ),
                                                ],
                                                color="primary",
                                                href="/table-page",
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
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
                                                "Here you can get insights into the data from various interactive charts.",
                                                className="card-text",
                                            ),
                                            dbc.Button(
                                                [
                                                    "To graphs ",
                                                    html.I(
                                                        className="bi bi-arrow-right"
                                                    ),
                                                ],
                                                color="primary",
                                                href="/graph-page",
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ]
            ),
        ]
    )
