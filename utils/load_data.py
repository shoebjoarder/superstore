import pandas as pd


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
    df_table = merged_df.copy(deep=True)

    return merged_df, df_original, df_table
