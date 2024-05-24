from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.exceptions import PreventUpdate
from typing import Any, Dict, List, Optional, Tuple

COLUMN_ORDER_DATE: str = "Order Date"
COLUMN_SHIP_DATE: str = "Ship Date"
COLUMN_DISCOUNT: str = "Discount"
COLUMN_PROFIT: str = "Profit"
COLUMN_QUANTITY: str = "Quantity"
COLUMN_RETURNED: str = "Returned"
COLUMN_SALES: str = "Sales"
COLUMN_SEGMENT: str = "Segment"
COLUMN_SHIP_MODE: str = "Ship Mode"
COLUMN_CUSTOMER_NAME: str = "Customer Name"
COLUMN_CATEGORY: str = "Category"
COLUMN_SUBCATEGORY: str = "Sub-Category"
COLUMN_PRODUCT_NAME: str = "Product Name"

DAYS_TO_SHIP: str = "Days to Ship"
PROFIT_RATIO: str = "Profit Ratio"


DROPDOWN_LIST: List[str] = [
    DAYS_TO_SHIP,
    COLUMN_DISCOUNT,
    COLUMN_PROFIT,
    PROFIT_RATIO,
    COLUMN_QUANTITY,
    COLUMN_RETURNED,
    COLUMN_SALES,
]

CATEGORICAL_DROPDOWN_LIST: List[str] = [
    COLUMN_RETURNED,
    COLUMN_SEGMENT,
    COLUMN_SHIP_MODE,
    COLUMN_CUSTOMER_NAME,
    COLUMN_CATEGORY,
    COLUMN_SUBCATEGORY,
    COLUMN_PRODUCT_NAME,
]

AXIS_DROPDOWN_LIST: List[str] = [
    DAYS_TO_SHIP,
    # COLUMN_RETURNED,
    COLUMN_DISCOUNT,
    COLUMN_PROFIT,
    PROFIT_RATIO,
    COLUMN_QUANTITY,
    COLUMN_SALES,
]

def graph_total(df: pd.DataFrame, value: str, date_key: str = "ME") -> pd.DataFrame:
    """
    Calculates the total sum of a specified column grouped by a date key.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be aggregated.
        value (str): The name of the column whose total sum is to be calculated.
        date_key (str, optional): The name of the column to use as the grouping key for aggregation. Defaults to "ME" (Monthly End).

    Returns:
        pd.DataFrame: A DataFrame with the total sum of the specified column, indexed by the date key.
    """
    return df.resample(date_key, on=COLUMN_ORDER_DATE)[value].sum().reset_index()


def graph_average(df: pd.DataFrame, value: str, date_key: str = "ME") -> pd.DataFrame:
    """
    Calculates the average percentage of a specified column grouped by a date key.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be averaged.
        value (str): The name of the column whose average percentage is to be calculated.
        date_key (str, optional): The name of the column to use as the grouping key for averaging. Defaults to "ME" (Monthly End).

    Returns:
        pd.DataFrame: A DataFrame with the average percentage of the specified column, indexed by the date key.
    """
    return (
        df.resample(date_key, on=COLUMN_ORDER_DATE)[value].mean().mul(100).reset_index()
    )


def graph_profit_ratio(df: pd.DataFrame, date_key: str = "ME") -> pd.DataFrame:
    """
    Calculates the profit ratio as a percentage of sales, monthly.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be analyzed.
        date_key (str, optional): The name of the column to use as the grouping key for calculation. Defaults to "ME" (Monthly End).

    Returns:
        pd.DataFrame: A DataFrame with the profit ratio as a percentage of sales, indexed by the date key.
    """
    grouped_profit_monthly = (
        df.resample(date_key, on=COLUMN_ORDER_DATE)[COLUMN_PROFIT].sum().reset_index()
    )
    grouped_sales_monthly = (
        df.resample(date_key, on=COLUMN_ORDER_DATE)[COLUMN_SALES].sum().reset_index()
    )
    merge_profit_sales = pd.merge(
        grouped_profit_monthly,
        grouped_sales_monthly,
        on=COLUMN_ORDER_DATE,
        how="outer",
    )
    merge_profit_sales[PROFIT_RATIO] = (
        merge_profit_sales[COLUMN_PROFIT] / merge_profit_sales[COLUMN_SALES]
    ) * 100
    return merge_profit_sales


def graph_returned(df: pd.DataFrame, date_key: str = "ME") -> pd.DataFrame:
    """
    Calculates the count of returned items per month.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be analyzed.
        date_key (str, optional): The name of the column to use as the grouping key for calculation. Defaults to "ME" (Monthly End).

    Returns:
        pd.DataFrame: A DataFrame with the count of returned items per period, indexed by the date key.
    """
    new_df = (
        df[df[COLUMN_RETURNED] == "Yes"]
        .groupby(COLUMN_ORDER_DATE)
        .size()
        .reset_index(name=COLUMN_RETURNED)
    )
    return (
        new_df.resample(date_key, on=COLUMN_ORDER_DATE)[COLUMN_RETURNED]
        .count()
        .reset_index()
    )


def graph_shipping(df: pd.DataFrame, date_key: str = "ME") -> pd.DataFrame:
    """
    Calculates the average days to ship per month.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be analyzed.
        date_key (str, optional): The name of the column to use as the grouping key for calculation. Defaults to "ME" (Monthly End).

    Returns:
        pd.DataFrame: A DataFrame with the average days to ship per period, indexed by the date key.
    """
    # df['Order Date'] = pd.to_datetime(df['Order Date'])
    df[COLUMN_SHIP_DATE] = pd.to_datetime(df[COLUMN_SHIP_DATE])
    df[DAYS_TO_SHIP] = (df[COLUMN_SHIP_DATE] - df[COLUMN_ORDER_DATE]).dt.days

    return (
        df.resample(date_key, on=COLUMN_ORDER_DATE)[DAYS_TO_SHIP].mean().reset_index()
    )


def plot_scatter(
    df: pd.DataFrame,
    x_axis_value: str,
    y_axis_value: str,
    categorical_value: str,
    new_x_axis_dropdown_list: List[str],
    new_y_axis_dropdown_list: List[str],
) -> go.Figure:
    """
    Generates a scatter plot and updates the dropdown options for the x and y axes.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be plotted.
        x_axis_value (str): The name of the column to use for the x-axis.
        y_axis_value (str): The name of the column to use for the y-axis.
        categorical_value (str): The name of the column to use for coloring the points in the scatter plot.
        new_x_axis_dropdown_list (List[str]): The list of available options for the x-axis dropdown menu.
        new_y_axis_dropdown_list (List[str]): The list of available options for the y-axis dropdown menu.

    Returns:
        go.Figure: A Plotly figure representing the scatter plot of the selected metrics.
    """
    return (
        px.scatter(
            df[[f"{x_axis_value}", f"{y_axis_value}", f"{categorical_value}"]],
            x=f"{x_axis_value}",
            y=f"{y_axis_value}",
            color=f"{categorical_value}",
        ),
        sorted(new_x_axis_dropdown_list),
        sorted(new_y_axis_dropdown_list),
    )


def insights_callbacks(app: Any) -> None:
    @app.callback(
        Output("dropdown-timeline-select-data", "options"),
        Output("dropdown-timeline-select-interval", "options"),
        Output("dropdown-timeline-select-data", "value"),
        Output("dropdown-timeline-select-interval", "value"),
        Output("dropdown-scatter-x-axis", "options"),
        Output("dropdown-scatter-y-axis", "options"),
        Output("dropdown-scatter-select-data", "options"),
        Output("dropdown-scatter-x-axis", "value"),
        Output("dropdown-scatter-y-axis", "value"),
        Output("dropdown-scatter-select-data", "value"),
        Output("insights-date-range", "min_date_allowed"),
        Output("insights-date-range", "max_date_allowed"),
        Output("insights-date-range", "initial_visible_month"),
        Input("dropdown-timeline-select-data", "options"),
        Input("memory-original", "data"),
    )
    def populate_dropdown_options(
        timeline_options: Optional[List[str]], memory_data: Dict[str, Any]
    ) -> Tuple[
        List[str], List[str], str, str, List[str], List[str], List[str], str, str, str
    ]:
        """
        Populates various dropdown menus and date range inputs based on the original memory data.

        Args:
            timeline_options (Optional[List[str]]): Current options for the timeline select data dropdown.
            memory_data (Dict[str, Any]): Original memory data containing information about different orders.

        Raises:
            PreventUpdate: If the timeline select data dropdown already has populated options, preventing further updates.

        Returns:
            Tuple[List[str], List[str], str, str, List[str], List[str], List[str], str, str, str, str, str, str]: A tuple containing the options and values for various dropdown menus and the minimum, maximum, and initial visible month for the insights date range.
        """
        if len(timeline_options) == 0:
            df = pd.DataFrame(memory_data).dropna()
            sorted_list = sorted(DROPDOWN_LIST)
            dropdown_date = ["Week", "Month", "Quarter", "Year"]
            sorted_axis_dropdown_list = sorted(AXIS_DROPDOWN_LIST)
            sorted_categorical_dropdown_list = sorted(CATEGORICAL_DROPDOWN_LIST)
            return (
                sorted_list,
                dropdown_date,
                sorted_list[1],
                dropdown_date[1],
                sorted_axis_dropdown_list,
                sorted_axis_dropdown_list,
                sorted_categorical_dropdown_list,
                sorted_axis_dropdown_list[4],
                sorted_axis_dropdown_list[2],
                sorted_categorical_dropdown_list[0],
                df[COLUMN_ORDER_DATE].min(),
                df[COLUMN_ORDER_DATE].max(),
                df[COLUMN_ORDER_DATE].max(),
            )
        else:
            raise PreventUpdate

    @app.callback(
        Output("insights-timeline-graph", "figure"),
        Input("dropdown-timeline-select-data", "value"),
        Input("dropdown-timeline-select-interval", "value"),
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-original", "data"),
        prevent_initial_call=True,
    )
    def input_linegraph_data(
        value: str,
        date_value: str,
        insights_date_range_start: Optional[str],
        insights_date_range_end: Optional[str],
        memory_data: Dict[str, Any],
    ) -> go.Figure:
        """
        Generates a line graph based on the selected dropdown values and date range.

        Args:
            value (str): The selected metric for the line graph.
            date_value (str): The selected interval for the line graph.
            insights_date_range_start (Optional[str]): The start date of the date range filter.
            insights_date_range_end (Optional[str]): The end date of the date range filter.
            memory_data (Dict[str, Any]): The original memory data containing information about different orders.

        Raises:
            PreventUpdate: If either the selected metric or interval is not specified, preventing the generation of the line graph.

        Returns:
            go.Figure: A Plotly figure representing the line graph of the selected metric over time.
        """

        if value is None or date_value is None:
            raise PreventUpdate
        else:
            dropdown_date = {
                "Week": "W",
                "Month": "ME",
                "Quarter": "QE",
                "Year": "YE",
            }
            date_key = dropdown_date[date_value]

            df = pd.DataFrame(memory_data).dropna()
            df[COLUMN_ORDER_DATE] = pd.to_datetime(df[COLUMN_ORDER_DATE])
            if (
                insights_date_range_start is not None
                and insights_date_range_end is not None
            ):
                df = df[
                    (df[COLUMN_ORDER_DATE] >= insights_date_range_start)
                    & (df[COLUMN_ORDER_DATE] <= insights_date_range_end)
                ]
            if value == COLUMN_DISCOUNT:
                return px.line(
                    graph_average(df, value, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=COLUMN_DISCOUNT,
                    title=f"{COLUMN_DISCOUNT} Trend",
                    markers=True,
                    labels={COLUMN_DISCOUNT: f"{COLUMN_DISCOUNT} (Avg %)"},
                )

            if value == COLUMN_RETURNED:
                return px.line(
                    graph_returned(df, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=COLUMN_RETURNED,
                    title=f"{COLUMN_RETURNED} Trend",
                    markers=True,
                    labels={COLUMN_RETURNED: f"{COLUMN_RETURNED} (Total)"},
                )

            if value == PROFIT_RATIO:
                return px.line(
                    graph_profit_ratio(df, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=PROFIT_RATIO,
                    title=f"{PROFIT_RATIO} Trend",
                    markers=True,
                    labels={PROFIT_RATIO: f"{PROFIT_RATIO} (%)"},
                )

            if value == DAYS_TO_SHIP:
                return px.line(
                    graphs_shipping(df, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=DAYS_TO_SHIP,
                    title=f"{DAYS_TO_SHIP} Trend",
                    markers=True,
                    labels={DAYS_TO_SHIP: f"{DAYS_TO_SHIP} (Avg)"},
                )

            if value == COLUMN_PROFIT:
                return px.line(
                    graph_total(df, value, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=COLUMN_PROFIT,
                    title=f"{COLUMN_PROFIT} Trend",
                    markers=True,
                    labels={COLUMN_PROFIT: f"{COLUMN_PROFIT} (Total)"},
                )

            if value == COLUMN_QUANTITY:
                return px.line(
                    graph_total(df, value, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=COLUMN_QUANTITY,
                    title=f"{COLUMN_QUANTITY} Trend",
                    markers=True,
                    labels={COLUMN_QUANTITY: f"{COLUMN_QUANTITY} (Total)"},
                )

            if value == COLUMN_SALES:
                return px.line(
                    graph_total(df, value, date_key),
                    x=COLUMN_ORDER_DATE,
                    y=COLUMN_SALES,
                    title=f"{COLUMN_SALES} Trend",
                    markers=True,
                    labels={COLUMN_SALES: f"{COLUMN_SALES} (Total)"},
                )

    @app.callback(
        Output("insights-scatterplot-graph", "figure"),
        Output("dropdown-scatter-x-axis", "options", allow_duplicate=True),
        Output("dropdown-scatter-y-axis", "options", allow_duplicate=True),
        Input("dropdown-scatter-x-axis", "value"),
        Input("dropdown-scatter-y-axis", "value"),
        Input("dropdown-scatter-select-data", "value"),
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-table", "data"),
        prevent_initial_call=True,
    )
    def input_scatterplot_graph(
        x_axis_value: str,
        y_axis_value: str,
        categorical_value: str,
        insights_date_range_start: Optional[str],
        insights_date_range_end: Optional[str],
        memory_data: Dict[str, Any],
    ) -> go.Figure:
        """
        Generates a scatter plot based on the selected dropdown values and date range.

        Args:
            x_axis_value (str): The selected metric for the x-axis of the scatter plot.
            y_axis_value (str): The selected metric for the y-axis of the scatter plot.
            categorical_value (str): The selected categorical variable for coloring the scatter plot points.
            insights_date_range_start (Optional[str]): The start date of the date range filter.
            insights_date_range_end (Optional[str]): The end date of the date range filter.
            memory_data (Dict[str, Any]): The original memory data containing information about different orders.

        Raises:
            PreventUpdate: If neither the x-axis nor y-axis values are specified, preventing the generation of the scatter plot.

        Returns:
            go.Figure: A Plotly figure representing the scatter plot of the selected metrics over time, colored by a categorical variable.
        """
        if x_axis_value is not None and y_axis_value is not None:
            new_x_axis_dropdown_list = [
                item for item in AXIS_DROPDOWN_LIST if item != y_axis_value
            ]
            new_y_axis_dropdown_list = [
                item for item in AXIS_DROPDOWN_LIST if item != x_axis_value
            ]
            df = pd.DataFrame(memory_data).dropna()
            df[COLUMN_ORDER_DATE] = pd.to_datetime(df[COLUMN_ORDER_DATE])
            df[COLUMN_SHIP_DATE] = pd.to_datetime(df[COLUMN_SHIP_DATE])
            df[DAYS_TO_SHIP] = (df[COLUMN_SHIP_DATE] - df[COLUMN_ORDER_DATE]).dt.days
            if (
                insights_date_range_start is not None
                and insights_date_range_end is not None
            ):
                df = df[
                    (df[COLUMN_ORDER_DATE] >= insights_date_range_start)
                    & (df[COLUMN_ORDER_DATE] <= insights_date_range_end)
                ]
            if x_axis_value == PROFIT_RATIO or y_axis_value == PROFIT_RATIO:
                df[PROFIT_RATIO] = (df[COLUMN_PROFIT] / df[COLUMN_SALES]) * 100
                return plot_scatter(
                    df,
                    x_axis_value,
                    y_axis_value,
                    categorical_value,
                    new_x_axis_dropdown_list,
                    new_y_axis_dropdown_list,
                )

            if x_axis_value == DAYS_TO_SHIP or y_axis_value == DAYS_TO_SHIP:
                return plot_scatter(
                    df,
                    x_axis_value,
                    y_axis_value,
                    categorical_value,
                    new_x_axis_dropdown_list,
                    new_y_axis_dropdown_list,
                )

            return plot_scatter(
                df,
                x_axis_value,
                y_axis_value,
                categorical_value,
                new_x_axis_dropdown_list,
                new_y_axis_dropdown_list,
            )
        else:
            raise PreventUpdate
