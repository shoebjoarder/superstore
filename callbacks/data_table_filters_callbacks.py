from dash import Output, Input, State
import pandas as pd


def filter_data(
    df,
    segment,
    ship_mode,
    ship_date_range_start,
    ship_date_range_end,
    order_date_range_start,
    order_date_range_end,
    category,
    subcategory,
    country,
    state,
    city,
):
    dataframe_table = df.dropna()
    count = 0
    temp = None
    temp_subcategory = sorted(dataframe_table["Sub-Category"].unique())
    temp_state = sorted(dataframe_table["State"].unique())
    temp_city = sorted(dataframe_table["City"].unique())

    if segment is not None:
        temp = dataframe_table[dataframe_table["Segment"] == segment]
        temp = temp.dropna(subset="Segment")

    if ship_mode is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table["Ship Mode"] == ship_mode].dropna(
                subset="Ship Mode"
            )
        else:
            temp = temp[temp["Ship Mode"] == ship_mode].dropna(subset=["Ship Mode"])

    if ship_date_range_start is not None and ship_date_range_end is not None:
        if temp is None:
            temp = dataframe_table[
                (dataframe_table["Ship Date"] >= ship_date_range_start)
                & (dataframe_table["Ship Date"] <= ship_date_range_end)
            ]
        else:
            temp = temp[
                (temp["Ship Date"] >= ship_date_range_start)
                & (temp["Ship Date"] <= ship_date_range_end)
            ]

    if order_date_range_start is not None and order_date_range_end is not None:
        if temp is None:
            temp = dataframe_table[
                (dataframe_table["Order Date"] >= order_date_range_start)
                & (dataframe_table["Order Date"] <= order_date_range_end)
            ]
        else:
            temp = temp[
                (temp["Order Date"] >= order_date_range_start)
                & (temp["Order Date"] <= order_date_range_end)
            ]

    if category is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table["Category"] == category].dropna(
                subset="Category"
            )
            temp_subcategory = sorted(temp["Sub-Category"].unique())
        else:
            temp = temp[temp["Category"] == category].dropna(subset=["Category"])
            temp_subcategory = sorted(temp["Sub-Category"].unique())

    if subcategory is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table["Sub-Category"] == subcategory
            ].dropna(subset="Sub-Category")
        else:
            temp = temp[temp["Sub-Category"] == subcategory]
            temp = temp.dropna(subset=["Sub-Category"])

    if country is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table["Country"] == country].dropna(
                subset="Country"
            )
            temp_state = sorted(temp["State"].unique())
            temp_city = sorted(temp["City"].unique())
        else:
            temp = temp[temp["Country"] == country].dropna(subset=["Country"])
            temp_state = sorted(temp["State"].unique())
            temp_city = sorted(temp["City"].unique())

    if state is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table["State"] == state].dropna(
                subset="State"
            )
            temp_city = sorted(temp["City"].unique())
        else:
            temp = temp[temp["State"] == state].dropna(subset=["State"])
            temp_city = sorted(temp["City"].unique())

    if city is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table["City"] == city].dropna(
                subset="City"
            )
        else:
            temp = temp[temp["City"] == city].dropna(subset=["City"])

    return temp, count, temp_subcategory, temp_state, temp_city


def get_data_table_filters_callbacks(app):
    @app.callback(
        Output("submit-filter", "children"),
        Output("clear-filter", "disabled"),
        Output("dropdown-sub-category", "options"),
        Output("dropdown-state", "options"),
        Output("dropdown-city", "options"),
        Input("dropdown-segment", "value"),
        Input("dropdown-ship-mode", "value"),
        Input("ship-date-range", "start_date"),
        Input("ship-date-range", "end_date"),
        Input("order-date-range", "start_date"),
        Input("order-date-range", "end_date"),
        Input("dropdown-category", "value"),
        Input("dropdown-sub-category", "value"),
        Input("dropdown-country", "value"),
        Input("dropdown-state", "value"),
        Input("dropdown-city", "value"),
        Input("memory-output", "data"),
    )
    def select_filters(
        segment,
        ship_mode,
        ship_date_range_start,
        ship_date_range_end,
        order_date_range_start,
        order_date_range_end,
        category,
        subcategory,
        country,
        state,
        city,
        dataframe_data,
    ):
        temp, count, temp_subcategory, temp_state, temp_city = filter_data(
            pd.DataFrame(dataframe_data),
            segment,
            ship_mode,
            ship_date_range_start,
            ship_date_range_end,
            order_date_range_start,
            order_date_range_end,
            category,
            subcategory,
            country,
            state,
            city,
        )

        if temp is not None:
            count = len(temp)
            if count == 0:
                return (
                    f"No data found!",
                    False,
                    temp_subcategory,
                    temp_state,
                    temp_city,
                )
            return (
                f"Show {count} data",
                False,
                temp_subcategory,
                temp_state,
                temp_city,
            )
        else:
            return (
                "Apply Filters",
                True,
                temp_subcategory,
                temp_state,
                temp_city,
            )

    @app.callback(
        Output("data-table", "data", allow_duplicate=True),
        Input("submit-filter", "n_clicks"),
        State("dropdown-segment", "value"),
        State("dropdown-ship-mode", "value"),
        State("ship-date-range", "start_date"),
        State("ship-date-range", "end_date"),
        State("order-date-range", "start_date"),
        State("order-date-range", "end_date"),
        State("dropdown-category", "value"),
        State("dropdown-sub-category", "value"),
        State("dropdown-country", "value"),
        State("dropdown-state", "value"),
        State("dropdown-city", "value"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def apply_filters(
        n_clicks,
        segment,
        ship_mode,
        ship_date_range_start,
        ship_date_range_end,
        order_date_range_start,
        order_date_range_end,
        category,
        subcategory,
        country,
        state,
        city,
        dataframe_data,
    ):
        temp, _, _, _, _ = filter_data(
            pd.DataFrame(dataframe_data),
            segment,
            ship_mode,
            ship_date_range_start,
            ship_date_range_end,
            order_date_range_start,
            order_date_range_end,
            category,
            subcategory,
            country,
            state,
            city,
        )

        if temp is None:
            return dataframe_data

        return temp.to_dict("records")

    @app.callback(
        Output("data-table", "data"),
        Output("dropdown-segment", "value"),
        Output("dropdown-ship-mode", "value"),
        Output("ship-date-range", "start_date"),
        Output("ship-date-range", "end_date"),
        Output("order-date-range", "start_date"),
        Output("order-date-range", "end_date"),
        Output("dropdown-category", "value"),
        Output("dropdown-sub-category", "value"),
        Output("dropdown-country", "value"),
        Output("dropdown-state", "value"),
        Output("dropdown-city", "value"),
        Input("clear-filter", "n_clicks"),
        Input("memory-output", "data"),
    )
    def clear_filters(n_clicks, dataframe_data):

        return (
            dataframe_data,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
