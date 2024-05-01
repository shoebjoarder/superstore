from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
from typing import Any, Dict, List, Tuple, Optional


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
    df: pd.DataFrame, filtered_df: pd.DataFrame, column: str, value: str, operator: str
) -> pd.DataFrame:
    if value is not None:
        if filtered_df.empty:
            filtered_df = df[getattr(df[column], operator)(value)].dropna(subset=column)
        else:
            filtered_df = filtered_df[
                getattr(filtered_df[column], operator)(value)
            ].dropna(subset=[column])

    return filtered_df


def filter_data(
    df: pd.DataFrame,
    segment: str,
    ship_mode: str,
    ship_date_range_start: str,
    ship_date_range_end: str,
    order_date_range_start: str,
    order_date_range_end: str,
    category: str,
    subcategory: str,
    country: str,
    state: str,
    city: str,
) -> Tuple[pd.DataFrame, List[str], List[str], List[str]]:
    clean_df = df.dropna()
    filtered_df = pd.DataFrame({})
    filtered_subcategory: pd.DataFrame = sorted(clean_df[COLUMN_SUBCATEGORY].unique())
    filtered_state: pd.DataFrame = sorted(clean_df[COLUMN_STATE].unique())
    filtered_city: pd.DataFrame = sorted(clean_df[COLUMN_CITY].unique())

    filters: List[Tuple[str, str, str]] = [
        (COLUMN_SEGMENT, segment, "eq"),
        (COLUMN_SHIP_MODE, ship_mode, "eq"),
        (COLUMN_SHIP_DATE, ship_date_range_start, "ge"),
        (COLUMN_SHIP_DATE, ship_date_range_end, "le"),
        (COLUMN_ORDER_DATE, order_date_range_start, "ge"),
        (COLUMN_ORDER_DATE, order_date_range_end, "le"),
    ]

    for column, value, operator in filters:
        filtered_df = filter_dataframe(clean_df, filtered_df, column, value, operator)

    if category is not None:
        if filtered_df is None:
            filtered_df = clean_df[clean_df[COLUMN_CATEGORY] == category].dropna(
                subset=COLUMN_CATEGORY
            )
            filtered_subcategory = sorted(filtered_df[COLUMN_SUBCATEGORY].unique())
        else:
            filtered_df = filtered_df[filtered_df[COLUMN_CATEGORY] == category].dropna(
                subset=[COLUMN_CATEGORY]
            )
            filtered_subcategory = sorted(filtered_df[COLUMN_SUBCATEGORY].unique())

    if subcategory is not None:
        if filtered_df is None:
            filtered_df = clean_df[clean_df[COLUMN_SUBCATEGORY] == subcategory].dropna(
                subset=COLUMN_SUBCATEGORY
            )
        else:
            filtered_df = filtered_df[filtered_df[COLUMN_SUBCATEGORY] == subcategory]
            filtered_df = filtered_df.dropna(subset=[COLUMN_SUBCATEGORY])

    if country is not None:
        if filtered_df is None:
            filtered_df = clean_df[clean_df[COLUMN_COUNTRY] == country].dropna(
                subset=COLUMN_COUNTRY
            )
            filtered_state = sorted(filtered_df[COLUMN_STATE].unique())
            filtered_city = sorted(filtered_df[COLUMN_CITY].unique())
        else:
            filtered_df = filtered_df[filtered_df[COLUMN_COUNTRY] == country].dropna(
                subset=[COLUMN_COUNTRY]
            )
            filtered_state = sorted(filtered_df[COLUMN_STATE].unique())
            filtered_city = sorted(filtered_df[COLUMN_CITY].unique())

    if state is not None:
        if filtered_df is None:
            filtered_df = clean_df[clean_df[COLUMN_STATE] == state].dropna(
                subset=COLUMN_STATE
            )
            filtered_city = sorted(filtered_df[COLUMN_CITY].unique())
        else:
            filtered_df = filtered_df[filtered_df[COLUMN_STATE] == state].dropna(
                subset=[COLUMN_STATE]
            )
            filtered_city = sorted(filtered_df[COLUMN_CITY].unique())

    if city is not None:
        if filtered_df is None:
            filtered_df = clean_df[clean_df[COLUMN_CITY] == city].dropna(
                subset=COLUMN_CITY
            )
        else:
            filtered_df = filtered_df[filtered_df[COLUMN_CITY] == city].dropna(
                subset=[COLUMN_CITY]
            )

    return filtered_df, filtered_subcategory, filtered_state, filtered_city


def data_table_filters_callbacks(app: Any) -> None:
    @app.callback(
        Output("dropdown-filter-segment", "options"),
        Output("dropdown-filter-ship-mode", "options"),
        Output("filter-ship-date-range", "max_date_allowed"),
        Output("filter-ship-date-range", "initial_visible_month"),
        Output("filter-order-date-range", "max_date_allowed"),
        Output("filter-order-date-range", "initial_visible_month"),
        Output("dropdown-filter-category", "options"),
        Output("dropdown-filter-sub-category", "options"),
        Output("dropdown-filter-country", "options"),
        Output("dropdown-filter-state", "options"),
        Output("dropdown-filter-city", "options"),
        Input("memory-copy", "data"),
        State("dropdown-filter-segment", "options"),
    )
    def populate_filter_options(
        memory_data: Dict[str, Any], segment: List[str]
    ) -> Tuple[
        List[str],
        List[str],
        str,
        str,
        str,
        str,
        List[str],
        List[str],
        List[str],
        List[str],
        List[str],
    ]:
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
        Output("dropdown-filter-sub-category", "options", allow_duplicate=True),
        Output("dropdown-filter-state", "options", allow_duplicate=True),
        Output("dropdown-filter-city", "options", allow_duplicate=True),
        Input("dropdown-filter-segment", "value"),
        Input("dropdown-filter-ship-mode", "value"),
        Input("filter-ship-date-range", "start_date"),
        Input("filter-ship-date-range", "end_date"),
        Input("filter-order-date-range", "start_date"),
        Input("filter-order-date-range", "end_date"),
        Input("dropdown-filter-category", "value"),
        Input("dropdown-filter-sub-category", "value"),
        Input("dropdown-filter-country", "value"),
        Input("dropdown-filter-state", "value"),
        Input("dropdown-filter-city", "value"),
        Input("clear-filter", "n_clicks"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def select_filters(
        segment: str,
        ship_mode: str,
        ship_date_range_start: str,
        ship_date_range_end: str,
        order_date_range_start: str,
        order_date_range_end: str,
        category: str,
        subcategory: str,
        country: str,
        state: str,
        city: str,
        clear_n_click: int,
        memory_data: Dict[str, Any],
    ) -> Tuple[str, bool, List[str], List[str], List[str]]:
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
                filtered_df, filtered_subcategory, filtered_state, filtered_city = (
                    filter_data(
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
                )
                if filtered_df is not None:
                    if len(filtered_df) == 0:
                        return (
                            f"No data found!",
                            False,
                            filtered_subcategory,
                            filtered_state,
                            filtered_city,
                        )
                    return (
                        f"Show {len(filtered_df)} data",
                        False,
                        filtered_subcategory,
                        filtered_state,
                        filtered_city,
                    )
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate

    @app.callback(
        Output("memory-output", "data", allow_duplicate=True),
        Output("dropdown-filter-segment", "value"),
        Output("dropdown-filter-ship-mode", "value"),
        Output("filter-ship-date-range", "start_date"),
        Output("filter-ship-date-range", "end_date"),
        Output("filter-order-date-range", "start_date"),
        Output("filter-order-date-range", "end_date"),
        Output("dropdown-filter-category", "value"),
        Output("dropdown-filter-sub-category", "value"),
        Output("dropdown-filter-country", "value"),
        Output("dropdown-filter-state", "value"),
        Output("dropdown-filter-city", "value"),
        Output("clear-filter", "n_clicks"),
        Output("submit-filter", "children", allow_duplicate=True),
        Output("clear-filter", "disabled", allow_duplicate=True),
        Output("dropdown-filter-sub-category", "options", allow_duplicate=True),
        Output("dropdown-filter-state", "options", allow_duplicate=True),
        Output("dropdown-filter-city", "options", allow_duplicate=True),
        Input("clear-filter", "n_clicks"),
        Input("memory-copy", "data"),
        prevent_initial_call=True,
    )
    def clear_filters(n_clicks: Optional[int], memory_copy: Dict[str, Any]) -> Tuple[
        Dict[str, Any],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[int],
        str,
        bool,
        List[str],
        List[str],
        List[str],
    ]:
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
        State("dropdown-filter-segment", "value"),
        State("dropdown-filter-ship-mode", "value"),
        State("filter-ship-date-range", "start_date"),
        State("filter-ship-date-range", "end_date"),
        State("filter-order-date-range", "start_date"),
        State("filter-order-date-range", "end_date"),
        State("dropdown-filter-category", "value"),
        State("dropdown-filter-sub-category", "value"),
        State("dropdown-filter-country", "value"),
        State("dropdown-filter-state", "value"),
        State("dropdown-filter-city", "value"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def apply_filters(
        n_clicks: Optional[int],
        segment: Optional[str],
        ship_mode: Optional[str],
        ship_date_range_start: Optional[str],
        ship_date_range_end: Optional[str],
        order_date_range_start: Optional[str],
        order_date_range_end: Optional[str],
        category: Optional[str],
        subcategory: Optional[str],
        country: Optional[str],
        state: Optional[str],
        city: Optional[str],
        memory_data: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], Optional[int]]:
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
