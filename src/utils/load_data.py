import pandas as pd
import os


def load_dataset(url=None):
    df_orders = None
    df_returns = None
    if url is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "..", "data")
        excel_file_path = os.path.join(data_dir, "Sample - Superstore.xlsx")

        df_orders = pd.read_excel(excel_file_path, sheet_name="Orders")
        df_returns = pd.read_excel(excel_file_path, sheet_name="Returns")
        print("***** Local Excel file used to load dataset! *****")
    else:
        df_orders = pd.read_excel(url, sheet_name="Orders")
        df_returns = pd.read_excel(url, sheet_name="Returns")
        print("***** Fetched the Excel file from GitHub successfully! *****")

    # df_orders.sort_values("Order ID", inplace=True)
    # df_returns.sort_values("Order ID", inplace=True)

    merged_df = pd.merge(df_orders, df_returns, on="Order ID", how="outer")

    merged_df["Returned"] = merged_df["Returned"].fillna("No")

    merged_df["Order Date"] = merged_df["Order Date"].dt.strftime("%Y-%m-%d")
    merged_df["Ship Date"] = merged_df["Ship Date"].dt.strftime("%Y-%m-%d")

    merged_df = merged_df.drop("Row ID", axis=1)
    df_original = merged_df.copy(deep=True)
    df_table = merged_df.copy(deep=True)

    return df_table
