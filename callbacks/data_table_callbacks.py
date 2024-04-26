from dash import Input, Output


def data_table_callbacks(app):
    @app.callback(
        Output("data-table", "data", allow_duplicate=True),
        Input("memory-output", "data"),
        prevent_initial_call=True,
    )
    def populate_data_table(data):
        if data is None:
            return []
        else:
            return data
