from dash import Input, Output


def data_table_callbacks(app):
    @app.callback(
        Output("data-table", "data"),
        Input("memory-output", "data"),
    )
    def populate_data_table(data):
        if data is None:
            return []
        else:
            return data
