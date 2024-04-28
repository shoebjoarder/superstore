from dash import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate


def graph_total(df, value, date_key="ME"):
    return df.resample(date_key, on="Order Date")[value].sum().reset_index()


def graph_average(df, value, date_key="ME"):
    return df.resample(date_key, on="Order Date")[value].mean().mul(100).reset_index()


def graph_profit_ratio(df, value, date_key="ME"):
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
    merge_profit_sales[value] = (
        merge_profit_sales["Profit"] / merge_profit_sales["Sales"]
    ) * 100
    return merge_profit_sales


def graph_returned(df, value, date_key="ME"):
    new_df = df[df[value] == "Yes"].groupby("Order Date").size().reset_index(name=value)
    return new_df.resample(date_key, on="Order Date")[value].count().reset_index()


def graphs_shipping(df, value, date_key="ME"):
    # df['Order Date'] = pd.to_datetime(df['Order Date'])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    df[value] = (df["Ship Date"] - df["Order Date"]).dt.days

    return df.resample(date_key, on="Order Date")[value].mean().reset_index()


DROPDOWN_LIST = [
    "Days to Ship",
    "Discount",
    "Profit",
    "Profit Ratio",
    "Quantity",
    "Returned",
    "Sales",
]

CATEGORICAL_DROPDOWN_LIST = [
    "Returned",
    "Segment",
    "Ship Mode",
    "Customer Name",
    "Category",
    "Sub-Category",
    "Product Name",
]

AXIS_DROPDOWN_LIST = [
    "Days to Ship",
    # "Returned",
    "Discount",
    "Profit",
    "Profit Ratio",
    "Quantity",
    "Sales",
]


def insights_callbacks(app):
    @app.callback(
        Output("dropdown-timeline-graph", "options"),
        Output("dropdown-week-month-quarter-year", "options"),
        Output("dropdown-timeline-graph", "value"),
        Output("dropdown-week-month-quarter-year", "value"),
        Output("dropdown-scatter-x-axis", "options"),
        Output("dropdown-scatter-y-axis", "options"),
        Output("dropdown-scatter-categorical", "options"),
        Output("dropdown-scatter-x-axis", "value"),
        Output("dropdown-scatter-y-axis", "value"),
        Output("dropdown-scatter-categorical", "value"),
        Input("dropdown-timeline-graph", "options"),
    )
    def populate_dropdown_options(timeline_options):
        if len(timeline_options) == 0:
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
            )
        else:
            raise PreventUpdate

    @app.callback(
        Output("insights-timeline-graph", "figure"),
        Input("dropdown-timeline-graph", "value"),
        Input("dropdown-week-month-quarter-year", "value"),
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-copy", "data"),
        prevent_initial_call=True,
    )
    def input_linegraph_data(
        value,
        date_value,
        insights_date_range_start,
        insights_date_range_end,
        memory_data,
    ):
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
            df["Order Date"] = pd.to_datetime(df["Order Date"])
            if (
                insights_date_range_start is not None
                and insights_date_range_end is not None
            ):
                df = df[
                    (df["Order Date"] >= insights_date_range_start)
                    & (df["Order Date"] <= insights_date_range_end)
                ]
            if value == "Discount":
                return px.line(
                    graph_average(df, value, date_key),
                    x="Order Date",
                    y=f"{value}",
                    title=f"{value} Trend",
                    markers=True,
                    labels={value: f"{value} (Avg %)"},
                )

            if value == "Returned":
                return px.line(
                    graph_returned(df, value, date_key),
                    x="Order Date",
                    y=f"{value}",
                    title=f"{value} Trend",
                    markers=True,
                    labels={value: f"{value} (Total)"},
                )

            if value == "Profit Ratio":
                return px.line(
                    graph_profit_ratio(df, value, date_key),
                    x="Order Date",
                    y="Profit Ratio",
                    title=f"{value} Trend",
                    markers=True,
                    labels={value: f"{value} (%)"},
                )

            if value == "Days to Ship":
                return px.line(
                    graphs_shipping(df, value, date_key),
                    x="Order Date",
                    y=value,
                    title=f"{value} Trend",
                    markers=True,
                    labels={value: f"{value} (Avg)"},
                )

            return px.line(
                graph_total(df, value, date_key),
                x="Order Date",
                y=f"{value}",
                title=f"{value} Trend",
                markers=True,
                labels={value: f"{value} (Total)"},
            )

    @app.callback(
        Output("insights-scatterplot-graph", "figure"),
        Output("dropdown-scatter-x-axis", "options", allow_duplicate=True),
        Output("dropdown-scatter-y-axis", "options", allow_duplicate=True),
        Input("dropdown-scatter-x-axis", "value"),
        Input("dropdown-scatter-y-axis", "value"),
        Input("dropdown-scatter-categorical", "value"),
        Input("insights-date-range", "start_date"),
        Input("insights-date-range", "end_date"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def input_scatterplot_graph(
        x_axis_value,
        y_axis_value,
        categorical_value,
        insights_date_range_start,
        insights_date_range_end,
        memory_data,
    ):
        if x_axis_value is not None and y_axis_value is not None:
            new_x_axis_dropdown_list = [
                item for item in AXIS_DROPDOWN_LIST if item != y_axis_value
            ]
            new_y_axis_dropdown_list = [
                item for item in AXIS_DROPDOWN_LIST if item != x_axis_value
            ]
            df = pd.DataFrame(memory_data).dropna()
            df["Order Date"] = pd.to_datetime(df["Order Date"])
            df["Ship Date"] = pd.to_datetime(df["Ship Date"])
            df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days
            if (
                insights_date_range_start is not None
                and insights_date_range_end is not None
            ):
                df = df[
                    (df["Order Date"] >= insights_date_range_start)
                    & (df["Order Date"] <= insights_date_range_end)
                ]
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
                )
            
            if x_axis_value == "Days to Ship" or y_axis_value == "Days to Ship":

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
            )
        else:
            raise PreventUpdate
