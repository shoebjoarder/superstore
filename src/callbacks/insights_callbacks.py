from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def graph_discount_profit_quantity_sales(df, value, date_key="ME"):
    return df.resample(date_key, on="Order Date")[value].sum().reset_index()


def graph_profit_ratio(df, date_key="ME"):
    grouped_profit_monthly = (
        df.resample(date_key, on="Order Date")["Profit"].sum().reset_index()
    )
    grouped_sales_monthly = (
        df.resample(date_key, on="Order Date")["Sales"].sum().reset_index()
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


def graph_returned(df, date_key="ME"):
    new_df = (
        df[df["Returned"] == "Yes"]
        .groupby("Order Date")
        .size()
        .reset_index(name="Returned")
    )

    return new_df.resample(date_key, on="Order Date")["Returned"].count().reset_index()


def insights_callbacks(app):
    @app.callback(
        Output("insights-timeline-graph", "figure"),
        Output("dropdown-timeline-graph", "options"),
        Output("dropdown-week-month-quarter-year", "options"),
        Input("dropdown-timeline-graph", "value"),
        Input("dropdown-week-month-quarter-year", "value"),
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-output", "data"),
    )
    def input_linegraph_data(
        value,
        date_value,
        insights_date_range_start,
        insights_date_range_end,
        memory_data,
    ):
        dropdown_list = [
            # "Days to Ship",
            "Discount",
            "Profit",
            "Profit Ratio",
            "Quantity",
            "Returned",
            "Sales",
        ]
        dropdown_date = {
            "Week": "W",
            "Month": "ME",
            "Quarter": "QE",
            "Year": "YE",
        }
        list_dropdown_date = list(dropdown_date.keys())
        date_key = dropdown_date[date_value]

        df = pd.DataFrame(memory_data).dropna()
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        if (
            insights_date_range_start is not None
            and insights_date_range_end is not None
        ):
            df = df[
                (df["Order Date"] >= insights_date_range_start)
                & (df["Order Date"] <= insights_date_range_end)
            ]
        if (
            value == "Discount"
            or value == "Profit"
            or value == "Quantity"
            or value == "Sales"
        ):
            return (
                px.line(
                    graph_discount_profit_quantity_sales(df, value, date_key),
                    x="Order Date",
                    y=f"{value}",
                    title=f"{value} Trend",
                    markers=True,
                ),
                sorted(dropdown_list),
                list_dropdown_date,
            )
        if value == "Profit Ratio":
            return (
                px.line(
                    graph_profit_ratio(df, date_key),
                    x="Order Date",
                    y="Profit Ratio",
                    title=f"{value} Trend",
                    markers=True,
                    labels={"Profit Ratio": "Profit Ratio (%)"},
                ),
                sorted(dropdown_list),
                list_dropdown_date,
            )

        if value == "Returned":
            return (
                px.line(
                    graph_returned(df, date_key),
                    x="Order Date",
                    y="Returned",
                    title=f"{value} Trend",
                    markers=True,
                    labels={"Count": "Total Returns"},
                ),
                sorted(dropdown_list),
                list_dropdown_date,
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
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-output", "data"),
    )
    def input_scatterplot_graph(
        x_axis_value,
        y_axis_value,
        categorical_value,
        insights_date_range_start,
        insights_date_range_end,
        memory_data,
    ):
        axis_dropdown_list = [
            # "Days to Ship",
            # "Returned",
            "Discount",
            "Profit",
            "Profit Ratio",
            "Quantity",
            "Sales",
        ]
        categorical_dropdown_list = [
            "Returned",
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
            if (
                insights_date_range_start is not None
                and insights_date_range_end is not None
            ):
                df = df[
                    (df["Order Date"] >= insights_date_range_start)
                    & (df["Order Date"] <= insights_date_range_end)
                ]
            if (
                x_axis_value == "Discount"
                or x_axis_value == "Profit"
                or x_axis_value == "Quantity"
                or x_axis_value == "Sales"
                or y_axis_value == "Discount"
                or y_axis_value == "Profit"
                or y_axis_value == "Quantity"
                or y_axis_value == "Sales"
            ):
                if x_axis_value == "Profit Ratio" or y_axis_value == "Profit Ratio":
                    df["Profit Ratio"] = (df["Profit"] / df["Sales"]) * 100
                    return (
                        px.scatter(
                            df[
                                [
                                    f"{x_axis_value}",
                                    f"{y_axis_value}",
                                    f"{categorical_value}",
                                ]
                            ],
                            x=f"{x_axis_value}",
                            y=f"{y_axis_value}",
                            color=f"{categorical_value}",
                        ),
                        sorted(new_x_axis_dropdown_list),
                        sorted(new_y_axis_dropdown_list),
                        sorted(categorical_dropdown_list),
                    )

                return (
                    px.scatter(
                        df[
                            [
                                f"{x_axis_value}",
                                f"{y_axis_value}",
                                f"{categorical_value}",
                            ]
                        ],
                        x=f"{x_axis_value}",
                        y=f"{y_axis_value}",
                        color=f"{categorical_value}",
                    ),
                    sorted(new_x_axis_dropdown_list),
                    sorted(new_y_axis_dropdown_list),
                    sorted(categorical_dropdown_list),
                )

        return
