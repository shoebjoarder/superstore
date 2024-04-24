import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from dash import dcc, html
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import merged_df as df

dash.register_page(__name__, name="Insights", path="/graph-page")


# Calculate accumulated sales and profit ratio
accumulated_sales = df["Sales"].sum()
profit_ratio = df["Profit"].sum() / accumulated_sales

# Group by 'Month', then sum 'Sales' for each unique year-month combination
grouped_sales_monthly = df.resample("ME", on="Order Date")["Sales"].sum().reset_index()
# Rename the columns for clarity
grouped_sales_monthly.columns = ["Order Date", "Total Sales"]

# Create a line chart for sales and profit
plot_fig = px.line(
    grouped_sales_monthly, x="Order Date", y="Total Sales", title="Sales Trends"
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Insights"),
                        html.P(
                            "Interactive charts that provides in-depth insights for your analysis."
                        ),
                    ]
                ),
            ],
            className="mt-4 mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            [
                                "Discount",
                                "Profit",
                                "Profit Ratio",
                                "Quantity",
                                "Returns",
                                "Sales",
                            ],
                            id="dropdown-timeline-graph",
                        ),
                        dcc.Graph(id="timeline-graph", figure=plot_fig),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-5",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Days to Ship",
                                                "Discount",
                                                "Profit",
                                                "Profit Ratio",
                                                "Quantity",
                                                "Returns",
                                                "Sales",
                                            ],
                                            id="dropdown-x-axis",
                                            placeholder="Select x-axis",
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Discount",
                                                "Profit",
                                                "Profit Ratio",
                                                "Quantity",
                                                "Returns",
                                                "Sales",
                                            ],
                                            id="dropdown-y-axis",
                                            placeholder="Select y-axis",
                                        ),
                                    ],
                                    xs=4,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Segment",
                                                "Ship Mode",
                                                "Customer Name",
                                                "Category",
                                                "Sub-Category",
                                                "Product Name",
                                            ],
                                            id="dropdown-breakdown",
                                            placeholder="Select categorical data",
                                        ),
                                    ],
                                    xs=4,
                                ),
                            ]
                        ),
                        dcc.Graph(id="graph-scatterplot", figure=plot_fig),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-5",
                ),
            ],
        ),
    ]
)
