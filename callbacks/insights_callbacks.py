from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def insights_callbacks(app):
    @app.callback(
        Output("insights-timeline-graph", "figure"),
        Input("dropdown-timeline-graph", "value"),
        Input("memory-output", "data"),
    )
    def input_linegraph_data(value, memory_data):
        df = pd.DataFrame(memory_data).dropna()
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        if (
            value == "Discount"
            or value == "Profit"
            or value == "Quantity"
            or value == "Sales"
        ):
            grouped_discount_monthly = (
                df.resample("ME", on="Order Date")[value].sum().reset_index()
            )

            plot_fig = px.line(
                grouped_discount_monthly,
                x="Order Date",
                y=f"{value}",
                title=f"{value} Trend",
                markers=True,
            )

            return plot_fig
        if value == "Profit Ratio":
            grouped_profit_monthly = (
                df.resample("ME", on="Order Date")["Profit"].sum().reset_index()
            )
            grouped_sales_monthly = (
                df.resample("ME", on="Order Date")["Sales"].sum().reset_index()
            )
            merge_profit_sales = pd.merge(
                grouped_profit_monthly,
                grouped_sales_monthly,
                on="Order Date",
                how="outer",
            )
            merge_profit_sales["Profit Ratio"] = (
                merge_profit_sales["Profit"] / merge_profit_sales["Sales"]
            ) * 100
            plot_fig = px.line(
                merge_profit_sales,
                x="Order Date",
                y="Profit Ratio",
                title=f"{value} Trend",
                markers=True,
                labels={"Profit Ratio": "Profit Ratio (%)"},
            )

            return plot_fig

        if value == "Returned":
            grouped_returns_monthly = (
                df.resample("ME", on="Order Date")["Returned"].count().reset_index()
            )
            plot_fig = px.line(
                grouped_returns_monthly,
                x="Order Date",
                y="Returned",
                title=f"{value} Trend",
                markers=True,
                labels={"Returned": "Total Returns"},
            )
            return plot_fig
