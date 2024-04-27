from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate


def data_table_entry_callbacks(app):
    @app.callback(
        Output("submit-val", "disabled"),
        Input("input-order-id", "value"),
        Input("input-order-date", "date"),
        Input("input-customer-id", "value"),
        Input("input-product-id", "value"),
        Input("input-quantity", "value"),
        prevent_initial_call=True,
    )
    def enable_submit_button(order_id, order_date, customer_id, product_id, quantity):
        if order_id and order_date and customer_id and product_id and quantity:
            return False
        else:
            return True

    @app.callback(
        Output("container-button-basic", "children"),
        Output("data-table", "data", allow_duplicate=True),
        Output("memory-output", "data"),
        Input("submit-val", "n_clicks"),
        State("input-order-id", "value"),
        State("input-order-date", "date"),
        State("input-customer-id", "value"),
        State("input-product-id", "value"),
        State("input-quantity", "value"),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def add_data_on_submit_data(
        n_clicks,
        order_id,
        order_date,
        customer_id,
        product_id,
        quantity,
        memory_data,
    ):
        if n_clicks is None:
            raise PreventUpdate

        feedback_message = f'Order ID: "{order_id}", Order date: "{order_date}", Customer ID: "{customer_id}", Product ID: "{product_id}", Quantity: "{quantity}"'

        if (
            order_id is not None
            and order_date is not None
            and customer_id is not None
            and product_id is not None
            and quantity is not None
        ):
            new_data = {
                "Order ID": order_id,
                "Order Date": order_date,
                "Customer ID": customer_id,
                "Product ID": product_id,
                "Quantity": quantity,
            }

            df = pd.DataFrame(memory_data)

            df.loc[-1] = new_data
            df.index = df.index + 1
            df.sort_index(inplace=True)

            return (
                feedback_message,
                df.to_dict("records"),
                df.to_dict("records"),
            )
        return feedback_message, memory_data, memory_data

        # file_name = "updated_data.xlsx"

        # with pd.ExcelWriter(file_name) as writer:
        #     dataframe_table.to_excel(writer, sheet_name="Orders", index=False)
        # print("Exported to an excel sheet")

    @app.callback(
        Output("positioned-toast", "is_open"),
        [Input("submit-val", "n_clicks")],
        prevent_initial_call=True,
    )
    def feedback_status_on_submit(n):
        if n:
            return True
        return False
