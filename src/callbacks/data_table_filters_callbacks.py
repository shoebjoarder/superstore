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


def filter_dataframe(
    df: pd.DataFrame, column: str, value: str, operator: str
) -> pd.DataFrame:
    """Helper function to filter dataframe based on condition."""
    if value is not None:
        if operator == "==":
            return df[df[column] == value]
        if operator == ">=":
            return df[df[column] >= value]
        if operator == "<=":
            return df[df[column] <= value]
    return df


def filter_data(df, filters):
    """Apply multiple filters to a DataFrame."""
    filtered_df = df.dropna()
    for column, value, operator in filters:
        filtered_df = filter_dataframe(filtered_df, column, value, operator)
    return filtered_df


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
                filters = [
                    (COLUMN_SEGMENT, segment, "=="),
                    (COLUMN_SHIP_MODE, ship_mode, "=="),
                    (COLUMN_SHIP_DATE, ship_date_range_start, ">="),
                    (COLUMN_SHIP_DATE, ship_date_range_end, "<="),
                    (COLUMN_ORDER_DATE, order_date_range_start, ">="),
                    (COLUMN_ORDER_DATE, order_date_range_end, "<="),
                    (COLUMN_CATEGORY, category, "=="),
                    (COLUMN_SUBCATEGORY, subcategory, "=="),
                    (COLUMN_COUNTRY, country, "=="),
                    (COLUMN_STATE, state, "=="),
                    (COLUMN_CITY, city, "=="),
                ]

                filtered_df = filter_data(pd.DataFrame(memory_data), filters)

                if not filtered_df.empty:
                    count = len(filtered_df)
                    if count == 0:
                        return (
                            f"No data found!",
                            False,
                            filtered_df[COLUMN_SUBCATEGORY].unique(),
                            filtered_df[COLUMN_STATE].unique(),
                            filtered_df[COLUMN_CITY].unique(),
                        )
                    return (
                        f"Show {count} data",
                        False,
                        filtered_df[COLUMN_SUBCATEGORY].unique(),
                        filtered_df[COLUMN_STATE].unique(),
                        filtered_df[COLUMN_CITY].unique(),
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
            filters = [
                (COLUMN_SEGMENT, segment, "=="),
                (COLUMN_SHIP_MODE, ship_mode, "=="),
                (COLUMN_SHIP_DATE, ship_date_range_start, ">="),
                (COLUMN_SHIP_DATE, ship_date_range_end, "<="),
                (COLUMN_ORDER_DATE, order_date_range_start, ">="),
                (COLUMN_ORDER_DATE, order_date_range_end, "<="),
                (COLUMN_CATEGORY, category, "=="),
                (COLUMN_SUBCATEGORY, subcategory, "=="),
                (COLUMN_COUNTRY, country, "=="),
                (COLUMN_STATE, state, "=="),
                (COLUMN_CITY, city, "=="),
            ]
            filtered_df = filter_data(pd.DataFrame(memory_data), filters)

            if filtered_df.empty:
                raise PreventUpdate
            else:
                return filtered_df.to_dict("records"), None

        else:
            raise PreventUpdate
