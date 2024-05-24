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
    clean_df: pd.DataFrame,
    filtered_df: pd.DataFrame,
    column: str,
    value: str,
) -> pd.DataFrame:
    """
    Filters a DataFrame based on a specified column and value, updating the filtered DataFrame with the result.

    Args:
        clean_df (pd.DataFrame): The original DataFrame containing all data.
        filtered_df (pd.DataFrame): A DataFrame that has been potentially pre-filtered and passed to this function for further refinement.
        column (str): The name of the column to filter by.
        value (str): The value to match in the specified column.

    Returns:
        pd.DataFrame: The filtered DataFrame, which reflects the rows matching the specified column and value, excluding rows with missing values in the specified column.
    """
    if value is not None:
        if filtered_df.empty:
            filtered_df = clean_df[clean_df[column] == value].dropna(subset=column)
        else:
            filtered_df = filtered_df[filtered_df[column] == value].dropna(
                subset=[column]
            )
    return filtered_df


def filter_category_subcategory(
    clean_df: pd.DataFrame,
    filtered_df: pd.DataFrame,
    category: str,
    subcategory: str,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Filters a DataFrame based on category and subcategory, returning both the filtered DataFrame and a list of unique subcategories.

    Args:
        clean_df (pd.DataFrame): The original DataFrame containing all categories and subcategories.
        filtered_df (pd.DataFrame): A DataFrame that has been potentially pre-filtered and passed to this function for further refinement.
        category (Optional[str]): The category to filter the DataFrame by. If None, no category-based filtering is applied.
        subcategory (Optional[str]): The subcategory to filter the DataFrame by. If None, no subcategory-based filtering is applied.

    Returns:
        Tuple[pd.DataFrame, List[str]]: A tuple containing the final filtered DataFrame and a list of unique subcategories present in the filtered DataFrame.
    """
    filtered_df_copy = filtered_df.copy(deep=True)
    filtered_subcategory_options: List[str] = []
    if category is not None:
        filtered_df_copy = filter_dataframe(
            clean_df, filtered_df_copy, COLUMN_CATEGORY, category
        )
        filtered_subcategory_options = sorted(
            filtered_df_copy[COLUMN_SUBCATEGORY].unique()
        )
        if subcategory not in filtered_subcategory_options:
            subcategory = None
    else:
        filtered_subcategory_options: List[str] = sorted(
            clean_df[COLUMN_SUBCATEGORY].unique()
        )
    if subcategory is not None:
        filtered_df_copy = filter_dataframe(
            clean_df, filtered_df_copy, COLUMN_SUBCATEGORY, subcategory
        )

    return filtered_df_copy, filtered_subcategory_options


def filter_country_state_city(
    clean_df: pd.DataFrame,
    filtered_df: pd.DataFrame,
    country: str,
    state: str,
    city: str,
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Filters a DataFrame based on country, state, and city, returning the filtered DataFrame along with lists of unique states and cities.

    Args:
        clean_df (pd.DataFrame): The original DataFrame containing all countries, states, and cities.
        filtered_df (pd.DataFrame): A DataFrame that has been potentially pre-filtered and passed to this function for further refinement.
        country (str): The country to filter the DataFrame by. If None, no country-based filtering is applied.
        state (str): The state to filter the DataFrame by. If None, no state-based filtering is applied.
        city (str): The city to filter the DataFrame by. If None, no city-based filtering is applied.

    Returns:
        Tuple[pd.DataFrame, List[str], List[str]]: A tuple containing the final filtered DataFrame and lists of unique states and cities present in the filtered DataFrame.
    """

    filtered_df_copy = filtered_df.copy(deep=True)
    filtered_state_options: List[str] = sorted(clean_df[COLUMN_STATE].unique())
    filtered_city_options: List[str] = sorted(clean_df[COLUMN_CITY].unique())
    if country is not None:
        filtered_df_copy = filter_dataframe(
            clean_df, filtered_df_copy, COLUMN_COUNTRY, country
        )
        filtered_state_options = sorted(filtered_df_copy[COLUMN_STATE].unique())
        filtered_city_options = sorted(filtered_df_copy[COLUMN_CITY].unique())
        if state not in filtered_state_options:
            state = None
        if city not in filtered_city_options:
            city = None

    if state is not None:
        filtered_df_copy = filter_dataframe(
            clean_df, filtered_df_copy, COLUMN_STATE, state
        )
        filtered_city_options = sorted(filtered_df_copy[COLUMN_CITY].unique())
        if city not in filtered_city_options:
            city = None

    if city is not None:
        filtered_df_copy = filter_dataframe(
            clean_df, filtered_df_copy, COLUMN_CITY, city
        )

    return filtered_df_copy, filtered_state_options, filtered_city_options


def filter_date_range(
    clean_df: pd.DataFrame, filtered_df: pd.DataFrame, column: str, start: str, end: str
) -> pd.DataFrame:
    """
    Filters a DataFrame based on a specified date range within a given column, updating the filtered DataFrame with the result.

    Args:
        clean_df (pd.DataFrame): The original DataFrame containing all data.
        filtered_df (pd.DataFrame): A DataFrame that has been potentially pre-filtered and passed to this function for further refinement.
        column (str): The name of the column containing date values to filter by.
        start (str): The starting date of the range to filter by.
        end (str): The ending date of the range to filter by.

    Returns:
        pd.DataFrame: The filtered DataFrame, which reflects the rows where the specified column's date falls between the `start` and `end` dates.
    """
    if start is not None and end is not None:
        if not filtered_df.empty:
            filtered_df = filtered_df[
                (filtered_df[column] >= start) & (filtered_df[column] <= end)
            ]
        else:
            filtered_df = clean_df[
                (clean_df[column] >= start) & (clean_df[column] <= end)
            ]
    return filtered_df


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
        Input("memory-original", "data"),
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
        """
        Populates dropdowns and date ranges with dynamic options based on the selected segment.

        Args:
            memory_data (Dict[str, Any]): A dictionary containing the current memory data.
            segment (List[str]): A list of currently selected segments.

        Raises:
            PreventUpdate: If a segment is selected, preventing the update to avoid unnecessary recalculations.

        Returns:
            Tuple[List[str], List[str], str, str, str, str, List[str], List[str], List[str], List[str], List[str]]: A tuple containing lists of unique options for each dropdown menu and the maximum dates for ship and order date ranges.
        """
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
        Output("submit-filter", "disabled"),
        Output("clear-filter", "disabled"),
        Output("dropdown-filter-sub-category", "options", allow_duplicate=True),
        Output("dropdown-filter-sub-category", "value", allow_duplicate=True),
        Output("dropdown-filter-state", "options", allow_duplicate=True),
        Output("dropdown-filter-city", "options", allow_duplicate=True),
        Output("memory-filter", "data"),
        Input("clear-filter", "n_clicks"),
        Input("dropdown-filter-segment", "value"),
        Input("dropdown-filter-ship-mode", "value"),
        Input("dropdown-filter-category", "value"),
        Input("dropdown-filter-sub-category", "value"),
        Input("dropdown-filter-country", "value"),
        Input("dropdown-filter-state", "value"),
        Input("dropdown-filter-city", "value"),
        Input("filter-ship-date-range", "start_date"),
        Input("filter-ship-date-range", "end_date"),
        Input("filter-order-date-range", "start_date"),
        Input("filter-order-date-range", "end_date"),
        Input("memory-original", "data"),
        prevent_initial_call=True,
    )
    def select_filters(
        clear_n_click: int,
        segment: str,
        ship_mode: str,
        category: str,
        subcategory: str,
        country: str,
        state: str,
        city: str,
        ship_date_range_start: str,
        ship_date_range_end: str,
        order_date_range_start: str,
        order_date_range_end: str,
        memory_original: Dict[str, Any],
    ) -> Tuple[str, bool, List[str], List[str], List[str]]:
        """
        Updates UI elements based on filter selections and applies filters to the data.

        Args:
            clear_n_click (int): Number of times the clear button was clicked.
            segment (str): Selected segment value.
            ship_mode (str): Selected shipping mode value.
            category (str): Selected category value.
            subcategory (str): Selected subcategory value.
            country (str): Selected country value.
            state (str): Selected state value.
            city (str): Selected city value.
            ship_date_range_start (str): Start date of the ship date range.
            ship_date_range_end (str): End date of the ship date range.
            order_date_range_start (str): Start date of the order date range.
            order_date_range_end (str): End date of the order date range.
            memory_original (Dict[str, Any]): Original memory data.

        Raises:
            PreventUpdate: If the clear button is clicked, preventing the update to reset the filters and clear the memory.

        Returns:
            Tuple[str, bool, List[str], List[str], List[str]]: A tuple containing the label for the submit button, whether the submit button is disabled, and lists of options/values for sub-category, state, and city dropdowns, and the filtered data records.
        """
        filtered_df: pd.DataFrame = pd.DataFrame({})
        clean_df: pd.DataFrame = pd.DataFrame(memory_original).dropna()
        filtered_subcategory_options: List[str] = []
        filtered_state: List[str] = []
        filtered_city: List[str] = []

        if clear_n_click is None:
            if (
                segment
                or ship_mode
                or category
                or subcategory
                or country
                or state
                or city
                or ship_date_range_start
                or ship_date_range_end
                or order_date_range_start
                or order_date_range_end
            ):
                filters: List[Tuple[str, str]] = [
                    (COLUMN_SEGMENT, segment),
                    (COLUMN_SHIP_MODE, ship_mode),
                ]

                filters_date_range: List[Tuple[str, str, str]] = [
                    (COLUMN_SHIP_DATE, ship_date_range_start, ship_date_range_end),
                    (COLUMN_ORDER_DATE, order_date_range_start, order_date_range_end),
                ]

                for column, value in filters:
                    filtered_df = filter_dataframe(clean_df, filtered_df, column, value)

                filtered_df, filtered_subcategory_options = filter_category_subcategory(
                    clean_df, filtered_df, category, subcategory
                )

                filtered_df, filtered_state, filtered_city = filter_country_state_city(
                    clean_df,
                    filtered_df,
                    country,
                    state,
                    city,
                )

                for column, start, end in filters_date_range:
                    filtered_df = filter_date_range(
                        clean_df, filtered_df, column, start, end
                    )

                if filtered_df.empty:
                    return (
                        [f"No data found!"],
                        True,
                        False,
                        filtered_subcategory_options,
                        subcategory,
                        filtered_state,
                        filtered_city,
                        filtered_df.to_dict("records"),
                    )
                return (
                    [f"Show {len(filtered_df)} data"],
                    False,
                    False,
                    filtered_subcategory_options,
                    subcategory,
                    filtered_state,
                    filtered_city,
                    filtered_df.to_dict("records"),
                )
            else:
                return (
                    ["Apply Filters"],
                    True,
                    True,
                    sorted(clean_df[COLUMN_SUBCATEGORY].unique()),
                    subcategory,
                    sorted(clean_df[COLUMN_STATE].unique()),
                    sorted(clean_df[COLUMN_CITY].unique()),
                    filtered_df.to_dict("records"),
                )
        else:
            raise PreventUpdate

    @app.callback(
        Output("memory-table", "data", allow_duplicate=True),
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
        Input("memory-original", "data"),
        prevent_initial_call=True,
    )
    def clear_filters(
        n_clicks: Optional[int], memory_original: Dict[str, Any]
    ) -> Tuple[
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
        """
        Clears all filters and resets the UI to its initial state.

        Args:
            n_clicks (Optional[int]): Number of times the clear button was clicked. If None, indicates the initial call.
            memory_original (Dict[str, Any]): Original memory data.

        Raises:
            PreventUpdate: On the initial call to prevent unnecessary processing.

        Returns:
            Tuple[Dict[str, Any], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[int], str, bool, List[str], List[str], List[str]]: A tuple containing the original memory data, None for all filter values, "Apply Filters" as the submit button text, True for the clear button being disabled, and lists of unique subcategories, states, and cities from the original data.
        """
        if n_clicks is None:
            raise PreventUpdate
        else:
            original_df = pd.DataFrame(memory_original)
            return (
                memory_original,
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
                sorted(original_df[COLUMN_SUBCATEGORY].unique()),
                sorted(original_df[COLUMN_STATE].unique()),
                sorted(original_df[COLUMN_CITY].unique()),
            )

    @app.callback(
        Output("memory-table", "data", allow_duplicate=True),
        Output("submit-filter", "n_clicks"),
        Input("submit-filter", "n_clicks"),
        Input("memory-filter", "data"),
        prevent_initial_call=True,
    )
    def apply_filters(
        n_clicks: Optional[int],
        memory_filter: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], Optional[int]]:
        """
        Applies filters and updates the memory table with the filtered data.

        Args:
            n_clicks (Optional[int]): Number of times the submit filter button was clicked. If None, indicates the initial call.
            memory_filter (Dict[str, Any]): Filtered data to be displayed in the memory table.

        Raises:
            PreventUpdate: If the memory filter data is empty, preventing the update to avoid displaying an empty table.

        Returns:
            Tuple[Dict[str, Any], Optional[int]]: A tuple containing the filtered data to be displayed in the memory table and None for the submit filter button click count, indicating that the filters have been successfully applied.
        """
        if n_clicks is not None:
            if pd.DataFrame(memory_filter).empty:
                raise PreventUpdate
            else:
                return memory_filter, None

        else:
            raise PreventUpdate
