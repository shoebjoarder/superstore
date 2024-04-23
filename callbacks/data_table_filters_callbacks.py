from dash import Output, Input


def get_data_table_filters_callbacks(app):
    @app.callback(
        Output("dd-output-container", "children"), Input("dropdown-segment", "value")
    )
    def update_output(value):
        return f"You have selected {value}"
