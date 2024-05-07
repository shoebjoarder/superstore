from dash import Input, Output
from typing import Any, Dict, List


def data_table_callbacks(app: Any) -> None:
    @app.callback(
        Output("data-table", "data"),
        Input("memory-table", "data"),
    )
    def populate_data_table(memory_table: Dict[str, Any]) -> List[Dict[str, Any]]:
        if memory_table is None:
            return []
        else:
            return memory_table
