from dash import Input, Output
from typing import Any, Dict, List


def data_table_callbacks(app: Any) -> None:
    @app.callback(
        Output("data-table", "data"),
        Input("memory-output", "data"),
    )
    def populate_data_table(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if data is None:
            return []
        else:
            return data
