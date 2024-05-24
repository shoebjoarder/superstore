from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from typing import Any, Dict, Tuple


MONTHS: int = 12


def prepare_dataframe(memory_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Prepares a DataFrame from memory data, handling missing values and date conversion.

    Args:
        memory_data (Dict[str, Any]): A dictionary containing the memory data to be converted into a DataFrame.

    Returns:
        pd.DataFrame: A prepared DataFrame ready for further analysis, with missing values dropped and the "Order Date" column converted to datetime format.
    """
    df = pd.DataFrame(memory_data).dropna()
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


def calculate_metrics(df: pd.DataFrame, months: int) -> Tuple[float, float, float]:
    """
    Calculates accumulated sales, total profit, and profit ratio over a specified number of months.

    Args:
        df (pd.DataFrame): The input DataFrame containing sales and profit data.
        months (int): The number of months over which to calculate the metrics.

    Returns:
        Tuple[float, float, float]: A tuple containing the accumulated sales, total profit, and profit ratio over the specified number of months.
    """
    df_profit = resample_data(df, "Profit")
    df_sales = resample_data(df, "Sales")

    acc_sales = df_sales["Sales"][0:months].sum()
    total_profit = df_profit["Profit"][0:months].sum()
    profit_ratio = total_profit / acc_sales

    return acc_sales, total_profit, profit_ratio


def resample_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Resamples a DataFrame to aggregate data by month-end periods.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be resampled.
        column (str): The name of the column whose values will be summed up for each month-end period.

    Returns:
        pd.DataFrame: A DataFrame with aggregated data for the specified column, grouped by month-end periods and sorted by "Order Date".
    """
    return (
        df.resample("ME", on="Order Date")[column]
        .sum()
        .reset_index()
        .sort_values(by=["Order Date"], ascending=False)
    )


def create_graphs(df: pd.DataFrame, months: int) -> Tuple[go.Figure, go.Figure]:
    """
    Creates line graphs for sales and profit over a specified number of months.

    Args:
        df (pd.DataFrame): The input DataFrame containing the sales and profit data.
        months (int): The number of months over which to display the sales and profit trends.

    Returns:
        Tuple[go.Figure, go.Figure]: A tuple containing two Plotly figures: one for sales and one for profit.
    """
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


def dashboard_callbacks(app: Any) -> None:
    @app.callback(
        Output("accumulated-sales", "children"),
        Output("profit-ratio", "children"),
        Output("dashboard-sales-graph", "figure"),
        Output("dashboard-profit-graph", "figure"),
        Input("memory-table", "data"),
    )
    def populate_dashboard(
        memory_data: Dict[str, Any]
    ) -> Tuple[str, str, go.Figure, go.Figure]:
        """
        Populates the dashboard with accumulated sales, profit ratio, and corresponding graphs.

        Args:
            memory_data (Dict[str, Any]): The data stored in memory to be used for dashboard updates.

        Raises:
            PreventUpdate: If `memory_data` is empty, indicating that there is no data to process.

        Returns:
            Tuple[str, str, go.Figure, go.Figure]: A tuple containing formatted strings for accumulated sales and profit ratio, and the generated figures for sales and profit graphs.
        """
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
