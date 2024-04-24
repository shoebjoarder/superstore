from dash import Output, Input, State


def get_data_table_entry_callbacks(app):
    @app.callback(
        Output("submit-val", "disabled"),
        [
            Input("input-order-id", "value"),
            Input("input-order-date", "date"),
            Input("input-customer-id", "value"),
            Input("input-product-id", "value"),
            Input("input-quantity", "value"),
        ],
    )
    def enable_submit_button(order_id, order_date, customer_id, product_id, quantity):
        if order_id and order_date and customer_id and product_id and quantity:
            return False
        else:
            return True

    @app.callback(
        Output("container-button-basic", "children"),
        Input("submit-val", "n_clicks"),
        State("input-order-id", "value"),
        State("input-order-date", "date"),
        State("input-customer-id", "value"),
        State("input-product-id", "value"),
        State("input-quantity", "value"),
        prevent_initial_call=True,
    )
    def feedback_message_on_submit_data(
        n_clicks, order_id, order_date, customer_id, product_id, quantity
    ):
        return 'Order ID: "{}", Order date: "{}", Customer ID: "{}", Product ID: "{}", Quantity: "{}"'.format(
            order_id, order_date, customer_id, product_id, quantity
        )

    @app.callback(
        Output("positioned-toast", "is_open"),
        [Input("submit-val", "n_clicks")],
    )
    def feedback_status_on_submit(n):
        if n:
            return True
        return False
