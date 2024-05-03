import pandas as pd
import os
from typing import Optional
import logging


SHEET_ORDER = "Orders"
SHEET_RETURNS = "Returns"
COLUMN_SHIP_DATE = "Order Date"
COLUMN_ORDER_DATE = "Ship Date"
COLUMN_ORDER_ID = "Order ID"
COLUMN_RETURNED = "Returned"
COLUMN_COUNTRY = "Country"


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
    local_filename = "Sample - Superstore.xlsx"
    folder_name = "data"
    if url is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "..", folder_name)
        excel_file_path = os.path.join(data_dir, local_filename)

        df_orders = pd.read_excel(excel_file_path, sheet_name=SHEET_ORDER)
        df_returns = pd.read_excel(excel_file_path, sheet_name=SHEET_RETURNS)
        logging.info("******* Local Excel file used to load dataset! *******")
    else:
        df_orders = pd.read_excel(url, sheet_name=SHEET_ORDER)
        df_returns = pd.read_excel(url, sheet_name=SHEET_RETURNS)
        logging.info("***** Downloaded Excel file used to load dataset! *****")

    merged_df = pd.merge(df_orders, df_returns, on=COLUMN_ORDER_ID, how="outer")
    merged_df.rename(columns={"Country/Region": COLUMN_COUNTRY}, inplace=True)

    merged_df[COLUMN_RETURNED] = merged_df[COLUMN_RETURNED].fillna("No")

    merged_df[COLUMN_SHIP_DATE] = merged_df[COLUMN_SHIP_DATE].dt.strftime("%Y-%m-%d")
    merged_df[COLUMN_ORDER_DATE] = merged_df[COLUMN_ORDER_DATE].dt.strftime("%Y-%m-%d")

    merged_df = merged_df.drop("Row ID", axis=1)

    return merged_df
