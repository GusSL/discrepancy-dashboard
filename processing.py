import pandas as pd

# Cols to select on df_expected
cols_selected = [
    "Retail_Product_Color",
    "Retail_Product_Level1",
    "Retail_Product_Level1Name",
    "Retail_Product_Level2Name",
    "Retail_Product_Level3Name",
    "Retail_Product_Name",
    "Retail_Product_SKU",
    "Retail_Product_Size",
    "Retail_Product_Style",
    "Retail_SOHQTY",
]

# Calculate discrepancies
def get_discrepancy(df_expected, df_counted):
    """Calculates the discrepancies on two provided DataFrames:

    Parameters:
    - df_expected -> DataFrame: Stock On Hand provided by customer
    - df_counted -> DataFrame: ytem app data from Inventory

    Return:
    - discrepancy -> DataFrame: Table with discrepancies on stock quantities
    """
    # Select columns for SOH
    soh = df_expected[cols_selected]

    # Exclude RFID duplicates
    df_counted.drop_duplicates(subset="RFID", inplace=True)

    # Group by Retail_Product_SKU
    cycle_count = df_counted.groupby("Retail_Product_SKU")["RFID"].count()
    cycle_count = cycle_count.reset_index().rename(columns={"RFID": "Retail_CCQTY"})
    cycle_count["Retail_Product_SKU"] = cycle_count["Retail_Product_SKU"].astype(int)

    # Calculate discrepancy
    discrepancy = pd.merge(
        soh, cycle_count, on="Retail_Product_SKU", how="outer", indicator=True
    )

    # Clean Retail_CCQTY and Retail_SOHQTY
    discrepancy["Retail_SOHQTY"] = discrepancy["Retail_SOHQTY"].fillna(0).astype(int)
    discrepancy["Retail_CCQTY"] = discrepancy["Retail_CCQTY"].fillna(0).astype(int)

    # Calculate differences
    discrepancy["Diff"] = discrepancy["Retail_CCQTY"] - discrepancy["Retail_SOHQTY"]
    discrepancy.loc[discrepancy["Diff"] > 0, "Overs"] = discrepancy["Diff"]
    discrepancy.loc[discrepancy["Diff"] < 0, "Unders"] = discrepancy["Diff"] * (-1)
    discrepancy["Unders"] = discrepancy["Unders"].fillna(0).astype(int)
    discrepancy["Overs"] = discrepancy["Overs"].fillna(0).astype(int)

    return discrepancy
