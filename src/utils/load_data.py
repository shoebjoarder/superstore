import pandas as pd
import os
from typing import Optional
import logging

# Define constants for column names and messages
COLUMN_SHIP_DATE = "Order Date"
COLUMN_ORDER_DATE = "Ship Date"
COLUMN_ORDER_ID = "Order ID"
COLUMN_RETURNED = "Returned"


def load_dataset(url: Optional[str] = None) -> pd.DataFrame:
    """
    Load and merge the Orders and Returns datasets from an Excel file.

    Parameters:
    - url (Optional[str]): URL to fetch the Excel file from. If None, the local file is used.

    Returns:
    - pd.DataFrame: The merged DataFrame.
    """
    df_orders = None
    df_returns = None
    if url is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "..", "data")
        excel_file_path = os.path.join(data_dir, "Sample - Superstore.xlsx")

        df_orders = pd.read_excel(excel_file_path, sheet_name="Orders")
        df_returns = pd.read_excel(excel_file_path, sheet_name="Returns")
        logging.info("***** Local Excel file used to load dataset! *****")
    else:
        df_orders = pd.read_excel(url, sheet_name="Orders")
        df_returns = pd.read_excel(url, sheet_name="Returns")
        logging.info("***** Fetched the Excel file from GitHub successfully! *****")

    merged_df = pd.merge(df_orders, df_returns, on=COLUMN_ORDER_ID, how="outer")

    merged_df[COLUMN_RETURNED] = merged_df[COLUMN_RETURNED].fillna("No")

    merged_df[COLUMN_SHIP_DATE] = merged_df[COLUMN_SHIP_DATE].dt.strftime("%Y-%m-%d")
    merged_df[COLUMN_ORDER_DATE] = merged_df[COLUMN_ORDER_DATE].dt.strftime("%Y-%m-%d")

    merged_df = merged_df.drop("Row ID", axis=1)

    return merged_df
