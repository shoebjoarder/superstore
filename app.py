import pandas as pd
import dash
import dash_bootstrap_components as dbc
from callbacks import get_data_table_filters_callbacks, get_data_table_entry_callbacks
from components import sidebar_component, navbar_component


# Load the data
def load_dataset():
    df_orders = pd.read_excel("Sample - Superstore.xlsx", sheet_name="Orders")
    df_returns = pd.read_excel("Sample - Superstore.xlsx", sheet_name="Returns")

    # df_orders.sort_values("Order ID", inplace=True)
    # df_returns.sort_values("Order ID", inplace=True)

    merged_df = pd.merge(df_orders, df_returns, on="Order ID", how="outer")

    merged_df["Returned"] = merged_df["Returned"].fillna("No")

    merged_df = merged_df.drop("Row ID", axis=1)
    df_original = merged_df.copy(deep=True)

    return merged_df, df_original


merged_df, df_original = load_dataset()


# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    use_pages=True,
)


app.layout = dbc.Container(
    [
        dbc.Row([navbar_component()]),
        dbc.Row(
            [
                dbc.Col([sidebar_component()], lg=2),
                dbc.Col([dash.page_container], lg=10),
            ]
        ),
    ],
    fluid=True,
)

# Callbacks
get_data_table_filters_callbacks(app)
get_data_table_entry_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
