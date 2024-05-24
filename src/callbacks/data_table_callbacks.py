from dash import Input, Output
from typing import Any, Dict, List


def data_table_callbacks(app: Any) -> None:
    @app.callback(
        Output("data-table", "data"),
        Input("memory-table", "data"),
    )
    def populate_data_table(memory_table: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Updates the data table with data from the memory table.

        Args:
            memory_table (Dict[str, Any]): The current data stored in the memory table.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the data to be displayed in the data table. If the memory table is empty, an empty list is returned.
        """
        if memory_table is None:
            return []
        else:
            return memory_table
