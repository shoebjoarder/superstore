from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate


COLUMN_ORDER_DATE: str = "Order Date"
COLUMN_SHIP_DATE: str = "Ship Date"
COLUMN_SHIP_MODE: str = "Ship Mode"
COLUMN_SEGMENT: str = "Segment"
COLUMN_COUNTRY: str = "Country"
COLUMN_STATE: str = "State"
COLUMN_CITY: str = "City"
COLUMN_CATEGORY: str = "Category"
COLUMN_SUBCATEGORY: str = "Sub-Category"


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
    temp_subcategory = sorted(dataframe_table[COLUMN_SUBCATEGORY].unique())
    temp_state = sorted(dataframe_table[COLUMN_STATE].unique())
    temp_city = sorted(dataframe_table[COLUMN_CITY].unique())

    if segment is not None:
        temp = dataframe_table[dataframe_table[COLUMN_SEGMENT] == segment]
        temp = temp.dropna(subset=COLUMN_SEGMENT)

    if ship_mode is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_SHIP_MODE] == ship_mode
            ].dropna(subset=COLUMN_SHIP_MODE)
        else:
            temp = temp[temp[COLUMN_SHIP_MODE] == ship_mode].dropna(
                subset=[COLUMN_SHIP_MODE]
            )

    if ship_date_range_start is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_SHIP_DATE] >= ship_date_range_start
            ]
        else:
            temp = temp[temp[COLUMN_SHIP_DATE] >= ship_date_range_start]

    if ship_date_range_end is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_SHIP_DATE] <= ship_date_range_end
            ]
        else:
            temp = temp[temp[COLUMN_SHIP_DATE] <= ship_date_range_end]

    if order_date_range_start is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_ORDER_DATE] >= order_date_range_start
            ]
        else:
            temp = temp[temp[COLUMN_ORDER_DATE] >= order_date_range_start]

    if order_date_range_end is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_ORDER_DATE] <= order_date_range_end
            ]
        else:
            temp = temp[temp[COLUMN_ORDER_DATE] <= order_date_range_end]
    if category is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table[COLUMN_CATEGORY] == category].dropna(
                subset=COLUMN_CATEGORY
            )
            temp_subcategory = sorted(temp[COLUMN_SUBCATEGORY].unique())
        else:
            temp = temp[temp[COLUMN_CATEGORY] == category].dropna(
                subset=[COLUMN_CATEGORY]
            )
            temp_subcategory = sorted(temp[COLUMN_SUBCATEGORY].unique())

    if subcategory is not None:
        if temp is None:
            temp = dataframe_table[
                dataframe_table[COLUMN_SUBCATEGORY] == subcategory
            ].dropna(subset=COLUMN_SUBCATEGORY)
        else:
            temp = temp[temp[COLUMN_SUBCATEGORY] == subcategory]
            temp = temp.dropna(subset=[COLUMN_SUBCATEGORY])

    if country is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table[COLUMN_COUNTRY] == country].dropna(
                subset=COLUMN_COUNTRY
            )
            temp_state = sorted(temp[COLUMN_STATE].unique())
            temp_city = sorted(temp[COLUMN_CITY].unique())
        else:
            temp = temp[temp[COLUMN_COUNTRY] == country].dropna(subset=[COLUMN_COUNTRY])
            temp_state = sorted(temp[COLUMN_STATE].unique())
            temp_city = sorted(temp[COLUMN_CITY].unique())

    if state is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table[COLUMN_STATE] == state].dropna(
                subset=COLUMN_STATE
            )
            temp_city = sorted(temp[COLUMN_CITY].unique())
        else:
            temp = temp[temp[COLUMN_STATE] == state].dropna(subset=[COLUMN_STATE])
            temp_city = sorted(temp[COLUMN_CITY].unique())

    if city is not None:
        if temp is None:
            temp = dataframe_table[dataframe_table[COLUMN_CITY] == city].dropna(
                subset=COLUMN_CITY
            )
        else:
            temp = temp[temp[COLUMN_CITY] == city].dropna(subset=[COLUMN_CITY])

    return temp, count, temp_subcategory, temp_state, temp_city


def data_table_filters_callbacks(app):
    @app.callback(
        Output("dropdown-segment", "options"),
        Output("dropdown-ship-mode", "options"),
        Output("ship-date-range", "max_date_allowed"),
        Output("ship-date-range", "initial_visible_month"),
        Output("order-date-range", "max_date_allowed"),
        Output("order-date-range", "initial_visible_month"),
        Output("dropdown-category", "options"),
        Output("dropdown-sub-category", "options"),
        Output("dropdown-country", "options"),
        Output("dropdown-state", "options"),
        Output("dropdown-city", "options"),
        Input("memory-output", "data"),
        State("dropdown-segment", "options"),
    )
    def populate_filter_options(memory_data, segment):
        if len(segment) == 0:
            df = pd.DataFrame(memory_data).dropna()
            return (
                sorted(df[COLUMN_SEGMENT].unique()),
                sorted(df[COLUMN_SHIP_MODE].unique()),
                df[COLUMN_SHIP_DATE].max(),
                df[COLUMN_SHIP_DATE].max(),
                df[COLUMN_ORDER_DATE].max(),
                df[COLUMN_ORDER_DATE].max(),
                sorted(df[COLUMN_CATEGORY].unique()),
                sorted(df[COLUMN_SUBCATEGORY].unique()),
                sorted(df[COLUMN_COUNTRY].unique()),
                sorted(df[COLUMN_STATE].unique()),
                sorted(df[COLUMN_CITY].unique()),
            )
        else:
            raise PreventUpdate

    @app.callback(
        Output("submit-filter", "children"),
        Output("clear-filter", "disabled"),
        Output("dropdown-sub-category", "options", allow_duplicate=True),
        Output("dropdown-state", "options", allow_duplicate=True),
        Output("dropdown-city", "options", allow_duplicate=True),
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
        Input("clear-filter", "n_clicks"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
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
        clear_n_click,
        memory_data,
    ):
        if clear_n_click is None:

            if (
                segment
                or ship_mode
                or ship_date_range_start
                or ship_date_range_end
                or order_date_range_start
                or order_date_range_end
                or category
                or subcategory
                or country
                or state
                or city
            ):
                temp, count, temp_subcategory, temp_state, temp_city = filter_data(
                    pd.DataFrame(memory_data),
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
                if not temp.empty:
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
                raise PreventUpdate
        else:
            raise PreventUpdate

    @app.callback(
        Output("memory-output", "data", allow_duplicate=True),
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
        Output("clear-filter", "n_clicks"),
        Output("submit-filter", "children", allow_duplicate=True),
        Output("clear-filter", "disabled", allow_duplicate=True),
        Output("dropdown-sub-category", "options", allow_duplicate=True),
        Output("dropdown-state", "options", allow_duplicate=True),
        Output("dropdown-city", "options", allow_duplicate=True),
        Input("clear-filter", "n_clicks"),
        Input("memory-copy", "data"),
        prevent_initial_call=True,
    )
    def clear_filters(n_clicks, memory_copy):
        if n_clicks is None:
            raise PreventUpdate
        else:
            df = pd.DataFrame(memory_copy)
            return (
                memory_copy,
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
                None,
                "Apply Filters",
                True,
                sorted(df[COLUMN_SUBCATEGORY].unique()),
                sorted(df[COLUMN_STATE].unique()),
                sorted(df[COLUMN_CITY].unique()),
            )

    @app.callback(
        Output("memory-output", "data", allow_duplicate=True),
        Output("submit-filter", "n_clicks"),
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
        memory_data,
    ):
        if n_clicks is not None:
            temp, _, _, _, _ = filter_data(
                pd.DataFrame(memory_data),
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
            if temp.empty:
                raise PreventUpdate
            else:
                return temp.to_dict("records"), None

        else:
            raise PreventUpdate
