from dash import Output, Input, State
import pandas as pd
import time
import random
from dash.exceptions import PreventUpdate


def generate_order_id(country_code):
    current_year = time.strftime("%Y")
    unique_id = random.randint(100000, 999999)
    order_id = f"{country_code}-{current_year}-{unique_id}"
    return order_id


def data_table_entry_callbacks(app):
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
        order_date, ship_mode, customer_id, product_id, quantity, button_disabled
    ):
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
        Input("memory-output", "data"),
    )
    def populate_ship_mode_options(ship_mode_options, memory_data):
        if len(ship_mode_options) == 0:
            return sorted(pd.DataFrame(memory_data)["Ship Mode"].unique())
        else:
            raise PreventUpdate

    @app.callback(
        Output("container-button-basic", "children"),
        Output("positioned-toast", "is_open"),
        Output("positioned-toast", "header"),
        Output("positioned-toast", "icon"),
        Output("memory-output", "data", allow_duplicate=True),
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
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def add_data_on_submit_data(
        n_clicks,
        ship_mode,
        order_date,
        order_id,
        customer_id,
        product_id,
        quantity,
        memory_data,
    ):
        df = pd.DataFrame(memory_data)
        feedback_message = "Error: No data could be added"

        found_duplicate_product = df.loc[
            (df["Ship Mode"] == ship_mode)
            & (df["Order Date"] == order_date)
            & (df["Order ID"] == order_id)
            & (df["Customer ID"] == customer_id)
            & (df["Product ID"] == product_id)
        ]
        if not found_duplicate_product.empty:
            feedback_message = "Duplicate: Data already exists!"
            return (
                feedback_message,
                True,
                "Error",
                "danger",
                memory_data,
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
            new_data = {
                # ! Customer Order ID function
                # "Order ID": generate_order_id("US"),
                "Ship Mode": ship_mode,
                "Order Date": order_date,
                "Order ID": order_id,
                "Customer ID": customer_id,
                "Product ID": product_id,
                "Quantity": quantity,
                "Returned": "No",
            }

            # * Inferring the relevant product details based on the newest order
            found_product = df.loc[df["Product ID"] == product_id][:1].sort_values(
                by=["Order Date"], ascending=False
            )
            if not found_product.empty:
                new_data["Category"] = found_product["Category"].values[0]
                new_data["Sub-Category"] = found_product["Sub-Category"].values[0]
                new_data["Product Name"] = found_product["Product Name"].values[0]

            # ! Inferring the relevant customer details based on the newest order (Not recommended)
            found_user = df.loc[df["Customer ID"] == customer_id][:1].sort_values(
                by=["Order Date"], ascending=False
            )
            if not found_product.empty:
                new_data["Customer Name"] = found_user["Customer Name"].values[0]
                new_data["Segment"] = found_user["Segment"].values[0]
                new_data["Country"] = found_user["Country"].values[0]
                new_data["City"] = found_user["City"].values[0]
                new_data["State"] = found_user["State"].values[0]
                new_data["Postal Code"] = found_user["Postal Code"].values[0]
                new_data["Region"] = found_user["Region"].values[0]

            df.loc[-1] = new_data
            df.index = df.index + 1
            df.sort_index(inplace=True)

            return (
                feedback_message,
                True,
                "Data added successfully!",
                "success",
                df.to_dict("records"),
                None,
                None,
                None,
                None,
                None,
            )
        else:
            raise PreventUpdate

    #         # file_name = "updated_data.xlsx"

    #         # with pd.ExcelWriter(file_name) as writer:
    #         #     dataframe_table.to_excel(writer, sheet_name="Orders", index=False)
    #         # print("Exported to an excel sheet")
