from dash import Output, Input, State
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
from dash.exceptions import PreventUpdate


COLUMN_ORDER_ID: str = "Order ID"
COLUMN_ORDER_DATE: str = "Order Date"
COLUMN_SHIP_MODE: str = "Ship Mode"
COLUMN_CUSTOMER_ID: str = "Customer ID"
COLUMN_CUSTOMER_NAME: str = "Customer Name"
COLUMN_SEGMENT: str = "Segment"
COLUMN_COUNTRY: str = "Country"
COLUMN_STATE: str = "State"
COLUMN_CITY: str = "City"
COLUMN_POSTAL_CODE: str = "Postal Code"
COLUMN_REGION: str = "Region"
COLUMN_PRODUCT_ID: str = "Product ID"
COLUMN_CATEGORY: str = "Category"
COLUMN_SUBCATEGORY: str = "Sub-Category"
COLUMN_PRODUCT_NAME: str = "Product Name"
COLUMN_QUANTITY: str = "Quantity"
COLUMN_RETURNED: str = "Returned"


def add_product_details_to_dataframe(
    df: pd.DataFrame, product_id: str
) -> Dict[str, Any]:
    """
    Adds product details to the dataframe based on the ID of the product.

    Extracts and returns product details from a DataFrame based on the latest order associated with a given product ID.

    Args:
        df (pd.DataFrame): The DataFrame containing orders, expected to have columns for product IDs, categories, subcategories, and product names among others.
        product_id (str): The ID of the product whose details are to be extracted.

    Returns:
        Dict[str, Any]: A dictionary containing the category, subcategory, and product name of the product associated with the latest order. If no matching product is found, an empty dictionary is returned.
    """
    # * Inferring the relevant product details based on the latest order
    found_product = df.loc[df[COLUMN_PRODUCT_ID] == product_id][:1].sort_values(
        by=[COLUMN_ORDER_DATE], ascending=False
    )
    if not found_product.empty:
        return {
            COLUMN_CATEGORY: found_product["Category"].values[0],
            COLUMN_SUBCATEGORY: found_product["Sub-Category"].values[0],
            COLUMN_PRODUCT_NAME: found_product["Product Name"].values[0],
        }
    return {}


def add_customer_details_to_dataframe(
    df: pd.DataFrame, customer_id: str
) -> Dict[str, Any]:
    """
    Adds customer details to the DataFrame based on the ID of the customer.

    Args:
        df (pd.DataFrame): The DataFrame containing orders, expected to have columns for customer IDs, customer names, segments, countries, cities, states, postal codes, regions, and order dates among others.
        customer_id (str): The ID of the customer whose details are to be extracted.

    Returns:
        Dict[str, Any]: A dictionary containing the customer's name, segment, country, city, state, postal code, and region associated with the latest order. If no matching customer is found, an empty dictionary is returned.
    """
    # ! Inferring the relevant customer details based on the latest order (Not recommended)
    found_user = df.loc[df[COLUMN_CUSTOMER_ID] == customer_id][:1].sort_values(
        by=[COLUMN_ORDER_DATE], ascending=False
    )
    if not found_user.empty:
        return {
            COLUMN_CUSTOMER_NAME: found_user["Customer Name"].values[0],
            COLUMN_SEGMENT: found_user["Segment"].values[0],
            COLUMN_COUNTRY: found_user["Country"].values[0],
            COLUMN_CITY: found_user["City"].values[0],
            COLUMN_STATE: found_user["State"].values[0],
            COLUMN_POSTAL_CODE: found_user["Postal Code"].values[0],
            COLUMN_REGION: found_user["Region"].values[0],
        }
    return {}


def add_new_data_to_dataframe(
    dataframe: pd.DataFrame,
    ship_mode: str,
    order_date: str,
    order_id: str,
    customer_id: str,
    product_id: str,
    quantity: int,
) -> pd.DataFrame:
    """
    Adds new data to the DataFrame at the top of the list, including product and customer details.

    Args:
        dataframe (pd.DataFrame): The DataFrame to which the new data will be added.
        ship_mode (str): The shipment mode for the new order.
        order_date (str): The date of the new order.
        order_id (str): The ID of the new order.
        customer_id (str): The ID of the customer placing the new order.
        product_id (str): The ID of the product ordered.
        quantity (int): The quantity of the product ordered.

    Returns:
        pd.DataFrame: The original DataFrame with the new data at the top of the DataFrame
    """
    df = dataframe
    new_data = {
        COLUMN_SHIP_MODE: ship_mode,
        COLUMN_ORDER_DATE: order_date,
        COLUMN_ORDER_ID: order_id,
        COLUMN_CUSTOMER_ID: customer_id,
        COLUMN_PRODUCT_ID: product_id,
        COLUMN_QUANTITY: quantity,
        COLUMN_RETURNED: "No",
    }
    product_details = add_product_details_to_dataframe(df, product_id)
    new_data.update(product_details)

    customer_details = add_customer_details_to_dataframe(df, customer_id)
    new_data.update(customer_details)

    df.loc[-1] = new_data
    df.index = df.index + 1
    df.sort_index(inplace=True)

    return df


def data_table_entry_callbacks(app: Any) -> None:
    @app.callback(
        Output("submit-data-entry", "disabled"),
        Input("input-order-date", "date"),
        Input("input-ship-mode", "value"),
        Input("input-customer-id", "value"),
        Input("input-product-id", "value"),
        Input("input-quantity", "value"),
        Input("submit-data-entry", "disabled"),
        prevent_initial_call=True,
    )
    def enable_submit_button(
        order_date: str,
        ship_mode: str,
        customer_id: str,
        product_id: str,
        quantity: str,
        button_disabled: bool,
    ) -> bool:
        """
        Enables or disables the submit data entry button based on input fields.

        Args:
            order_date (str): The date of the order.
            ship_mode (str): The shipping mode.
            customer_id (str): The ID of the customer.
            product_id (str): The ID of the product.
            quantity (str): The quantity of the product.
            button_disabled (bool): Whether the submit button is currently disabled.

        Raises:
            PreventUpdate: To prevent unnecessary updates if the submit button should remain disabled.

        Returns:
            bool: True if the submit button should be enabled, False otherwise.
        """
        if order_date and ship_mode and customer_id and product_id and quantity:
            if button_disabled == True:
                return False
            else:
                raise PreventUpdate
        elif button_disabled == True:
            raise PreventUpdate
        else:
            return True

    @app.callback(
        Output("input-ship-mode", "options"),
        Input("input-ship-mode", "options"),
        Input("memory-original", "data"),
    )
    def populate_ship_mode_options(
        ship_mode_options: List[Dict], memory_original: Dict[str, Any]
    ):
        """
        Populates the ship mode options dropdown based on the original memory data.

        Args:
            ship_mode_options (List[Dict]): Current options for the ship mode dropdown.
            memory_original (Dict[str, Any]): Original memory data containing information about different ship modes.

        Raises:
            PreventUpdate: If the ship mode options dropdown already has populated options, preventing further updates.

        Returns:
            List[Dict]: Updated options for the ship mode dropdown, populated with unique ship modes from the original memory data if the dropdown was initially empty.
        """
        if len(ship_mode_options) == 0:
            # return {
            #     item: item
            #     for item in sorted(
            #         pd.DataFrame(memory_original)[COLUMN_SHIP_MODE].unique()
            #     )
            # }
            return sorted(pd.DataFrame(memory_original)[COLUMN_SHIP_MODE].unique())
        else:
            raise PreventUpdate

    @app.callback(
        Output("data-entry-feedback", "children"),
        Output("data-entry-feedback-toast", "is_open"),
        Output("data-entry-feedback-toast", "header"),
        Output("data-entry-feedback-toast", "icon"),
        Output("memory-table", "data", allow_duplicate=True),
        Output("memory-original", "data", allow_duplicate=True),
        Output("input-ship-mode", "value"),
        Output("input-order-id", "value"),
        Output("input-customer-id", "value"),
        Output("input-product-id", "value"),
        Output("input-quantity", "value"),
        Input("submit-data-entry", "n_clicks"),
        State("input-ship-mode", "value"),
        State("input-order-date", "date"),
        State("input-order-id", "value"),
        State("input-customer-id", "value"),
        State("input-product-id", "value"),
        State("input-quantity", "value"),
        Input("memory-table", "data"),
        Input("memory-original", "data"),
        prevent_initial_call=True,
    )
    def add_data_on_submit_data(
        n_clicks: Optional[int],
        ship_mode: str,
        order_date: str,
        order_id: str,
        customer_id: str,
        product_id: str,
        quantity: str,
        memory_table: Dict[str, Any],
        memory_original: Dict[str, Any],
    ) -> Tuple[
        str,
        bool,
        str,
        str,
        Dict[str, Any],
        Dict[str, Any],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        """
        Handles the submission of new data entries and provides feedback.

        Args:
            n_clicks (Optional[int]): Number of times the submit button was clicked. If None, indicates the initial call.
            ship_mode (str): Shipping mode selected for the new order.
            order_date (str): Date of the new order.
            order_id (str): Unique identifier for the new order.
            customer_id (str): Identifier for the customer placing the new order.
            product_id (str): Identifier for the product being ordered.
            quantity (str): Quantity of the product being ordered.
            memory_table (Dict[str, Any]): Current data stored in the memory table.
            memory_original (Dict[str, Any]): Original data set.

        Raises:
            PreventUpdate: If the form is submitted without filling out all required fields, preventing further updates.

        Returns:
            Tuple[str, bool, str, str, Dict[str, Any], Dict[str, Any], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]: A tuple containing the feedback message, a boolean indicating if the toast should be open, the header and icon for the toast, the updated data for the memory table and original memory data, and the values of the input fields after submission.
        """
        df = pd.DataFrame(memory_table)
        df_original = pd.DataFrame(memory_original)
        feedback_message = "Error: No data could be added"

        found_duplicate_product = df.loc[
            (df[COLUMN_ORDER_ID] == order_id)
            & (df[COLUMN_CUSTOMER_ID] == customer_id)
            & (df[COLUMN_PRODUCT_ID] == product_id)
        ]
        if not found_duplicate_product.empty:
            feedback_message = "Duplicate: Data already exists!"
            return (
                feedback_message,
                True,
                "Error",
                "danger",
                memory_table,
                memory_original,
                ship_mode,
                order_id,
                customer_id,
                product_id,
                quantity,
            )
        elif (
            ship_mode is not None
            and order_date is not None
            and order_id is not None
            and customer_id is not None
            and product_id is not None
            and quantity is not None
        ):
            feedback_message = f'Order date: "{order_date}", Ship Mode: "{ship_mode}", Order ID: "{order_id}", Customer ID: "{customer_id}", Product ID: "{product_id}", Quantity: "{quantity}"'
            df = add_new_data_to_dataframe(
                df, ship_mode, order_date, order_id, customer_id, product_id, quantity
            )
            df_original = add_new_data_to_dataframe(
                df_original,
                ship_mode,
                order_date,
                order_id,
                customer_id,
                product_id,
                quantity,
            )

            return (
                feedback_message,
                True,
                "Data added successfully!",
                "success",
                df.to_dict("records"),
                df_original.to_dict("records"),
                None,
                None,
                None,
                None,
                None,
            )
        else:
            raise PreventUpdate


# TODO: Enhance the data table with Download file feature
# file_name = "updated_data.xlsx"

# with pd.ExcelWriter(file_name) as writer:
#     dataframe_table.to_excel(writer, sheet_name="Orders", index=False)
# print("Exported to an excel sheet")
