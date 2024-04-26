from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px


def dashboard_callbacks(app):
    @app.callback(
        Output("accumulated-sales", "children"),
        Output("profit-ratio", "children"),
        Output("dashboard-sales-graph", "figure"),
        Output("dashboard-profit-graph", "figure"),
        Input("memory-output", "data"),
    )
    def populate_dashboard(memory_data):
        df = pd.DataFrame(memory_data).dropna()
        df["Order Date"] = pd.to_datetime(df["Order Date"])

        most_recent_date = df["Order Date"].max()
        four_months_ago = most_recent_date - pd.Timedelta(days=120)

        # Now, the comparison should work without errors
        recent_data = df[
            (df["Order Date"] >= four_months_ago)
            & (df["Order Date"] <= most_recent_date)
        ]

        # Calculate accumulated sales and profit ratio
        accumulated_sales = recent_data["Sales"].sum()
        profit_ratio = df["Profit"].sum() / accumulated_sales

        print(f"${accumulated_sales:,.2f}")

        # Group by 'Month', then sum 'Sales' for each unique year-month combination
        grouped_sales_monthly = (
            recent_data.resample("ME", on="Order Date")["Sales"].sum().reset_index()
        )
        grouped_profit_monthly = (
            recent_data.resample("ME", on="Order Date")["Profit"].sum().reset_index()
        )

        # Create a line chart for sales and profit
        sales_fig = px.line(
            grouped_sales_monthly,
            x="Order Date",
            y="Sales",
            title="Sales Trends",
            labels={"Sales": "Total Sales"},
        )
        profit_fig = px.line(
            grouped_profit_monthly,
            x="Order Date",
            y="Profit",
            title="Profit Trends",
            labels={"Profit": "Total Profit"},
        )
        return (
            f"${accumulated_sales:,.2f}",
            f"{profit_ratio:.2%}",
            sales_fig,
            profit_fig,
        )
