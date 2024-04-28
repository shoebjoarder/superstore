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

        months = 12
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df_profit = (
            df.resample("ME", on="Order Date")["Profit"]
            .sum()
            .reset_index()
            .sort_values(by=["Order Date"], ascending=False)
        )
        df_sales = (
            df.resample("ME", on="Order Date")["Sales"]
            .sum()
            .reset_index()
            .sort_values(by=["Order Date"], ascending=False)
        )

        acc_sales = df_sales["Sales"][0:months].sum()
        total_profit = df_profit["Profit"][0:months].sum()
        profit_ratio = total_profit / acc_sales

        # Create a line chart for sales and profit
        sales_fig = px.line(
            df_sales[0:months],
            x="Order Date",
            y="Sales",
            # title="Sales Trends",
            labels={"Sales": "Total Sales"},
        )
        profit_fig = px.line(
            df_profit[0:months],
            x="Order Date",
            y="Profit",
            # title="Profit Trends",
            labels={"Profit": "Total Profit"},
        )
        return (
            f"${acc_sales:,.2f}",
            f"{profit_ratio:.2%}",
            sales_fig,
            profit_fig,
        )
