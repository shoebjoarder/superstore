from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from typing import Any, Dict, Tuple


MONTHS: int = 12


def dashboard_callbacks(app: Any) -> None:
    @app.callback(
        Output("accumulated-sales", "children"),
        Output("profit-ratio", "children"),
        Output("dashboard-sales-graph", "figure"),
        Output("dashboard-profit-graph", "figure"),
        Input("memory-output", "data"),
    )
    def populate_dashboard(
        memory_data: Dict[str, Any]
    ) -> Tuple[str, str, go.Figure, go.Figure]:
        if not memory_data:
            raise PreventUpdate

        df = prepare_dataframe(memory_data)
        acc_sales, _, profit_ratio = calculate_metrics(df, MONTHS)
        sales_fig, profit_fig = create_graphs(df, MONTHS)

        return (
            f"${acc_sales:,.2f}",
            f"{profit_ratio:.2%}",
            sales_fig,
            profit_fig,
        )


def prepare_dataframe(memory_data: Dict[str, Any]) -> pd.DataFrame:
    """Prepare the DataFrame from memory data."""
    df = pd.DataFrame(memory_data).dropna()
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


def calculate_metrics(df: pd.DataFrame, months: int) -> Tuple[float, float, float]:
    """Calculate the accumulated sales, total profit, and profit ratio."""
    df_profit = resample_data(df, "Profit")
    df_sales = resample_data(df, "Sales")

    acc_sales = df_sales["Sales"][0:MONTHS].sum()
    total_profit = df_profit["Profit"][0:MONTHS].sum()
    profit_ratio = total_profit / acc_sales

    return acc_sales, total_profit, profit_ratio


def resample_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Resample data for a given column"""
    return (
        df.resample("ME", on="Order Date")[column]
        .sum()
        .reset_index()
        .sort_values(by=["Order Date"], ascending=False)
    )


def create_graphs(df: pd.DataFrame, months: int) -> Tuple[go.Figure, go.Figure]:
    df_profit = resample_data(df, "Profit")
    df_sales = resample_data(df, "Sales")

    sales_fig = px.line(
        df_sales[0:months],
        x="Order Date",
        y="Sales",
        labels={"Sales": "Total Sales"},
    )
    profit_fig = px.line(
        df_profit[0:months],
        x="Order Date",
        y="Profit",
        labels={"Profit": "Total Profit"},
    )
    return sales_fig, profit_fig
