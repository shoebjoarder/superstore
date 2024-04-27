from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def graph_discount_profit_quantity_sales(df, value):
    return df.resample("ME", on="Order Date")[value].sum().reset_index()


def graph_profit_ratio(df):
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
    return merge_profit_sales


def graph_returned(df):
    return df.resample("ME", on="Order Date")["Returned"].count().reset_index()


def insights_callbacks(app):
    @app.callback(
        Output("insights-timeline-graph", "figure"),
        Output("dropdown-timeline-graph", "options"),
        Input("dropdown-timeline-graph", "value"),
        Input("memory-output", "data"),
    )
    def input_linegraph_data(value, memory_data):
        dropdown_list = [
            # "Days to Ship",
            "Discount",
            "Profit",
            "Profit Ratio",
            "Quantity",
            "Returned",
            "Sales",
        ]
        df = pd.DataFrame(memory_data).dropna()
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        if (
            value == "Discount"
            or value == "Profit"
            or value == "Quantity"
            or value == "Sales"
        ):
            return (
                px.line(
                    graph_discount_profit_quantity_sales(df, value),
                    x="Order Date",
                    y=f"{value}",
                    title=f"{value} Trend",
                    markers=True,
                ),
                dropdown_list,
            )
        if value == "Profit Ratio":
            return (
                px.line(
                    graph_profit_ratio(df),
                    x="Order Date",
                    y="Profit Ratio",
                    title=f"{value} Trend",
                    markers=True,
                    labels={"Profit Ratio": "Profit Ratio (%)"},
                ),
                dropdown_list,
            )

        if value == "Returned":
            return (
                px.line(
                    graph_returned(df),
                    x="Order Date",
                    y="Returned",
                    title=f"{value} Trend",
                    markers=True,
                    labels={"Returned": "Total Returns"},
                ),
                dropdown_list,
            )
        if value is None:
            return

    @app.callback(
        Output("insights-scatterplot-graph", "figure"),
        Output("dropdown-scatter-x-axis", "options"),
        Output("dropdown-scatter-y-axis", "options"),
        Output("dropdown-scatter-categorical", "options"),
        Input("dropdown-scatter-x-axis", "value"),
        Input("dropdown-scatter-y-axis", "value"),
        Input("dropdown-scatter-categorical", "value"),
        Input("memory-output", "data"),
    )
    def input_scatterplot_graph(
        x_axis_value, y_axis_value, categorical_value, memory_data
    ):
        axis_dropdown_list = [
            # "Days to Ship",
            "Discount",
            "Profit",
            "Profit Ratio",
            "Quantity",
            "Returns",
            "Sales",
        ]
        categorical_dropdown_list = [
            "Segment",
            "Ship Mode",
            "Customer Name",
            "Category",
            "Sub-Category",
            "Product Name",
        ]
        new_x_axis_dropdown_list = [
            item for item in axis_dropdown_list if item != y_axis_value
        ]
        new_y_axis_dropdown_list = [
            item for item in axis_dropdown_list if item != x_axis_value
        ]

        if x_axis_value is not None and y_axis_value is not None:
            df = pd.DataFrame(memory_data).dropna()
            df["Order Date"] = pd.to_datetime(df["Order Date"])

            return (
                px.scatter(
                    df[[f"{x_axis_value}", f"{y_axis_value}", f"{categorical_value}"]],
                    x=f"{x_axis_value}",
                    y=f"{y_axis_value}",
                    color=f"{categorical_value}",
                ),
                new_x_axis_dropdown_list,
                new_y_axis_dropdown_list,
                categorical_dropdown_list,
            )
        return
