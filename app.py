import streamlit as st
import matplotlib.pyplot as plt

from helper import get_statistics_as_markdown, upload_csv_file
from processing import get_discrepancy

# Config
st.set_page_config(layout="wide", page_title="Stock/Inventory Discrepancies")

st.header("Stock/Inventory Discrepancy Automated Analysis")

df_expected = df_counted = None
file_readers = st.empty()

# Import data from files
if df_expected is None or df_counted is None:
    col1, col2 = file_readers.columns(2)

    file_expected, df_expected = upload_csv_file(
        "Upload customer data (expected Stock On Hand)", col1
    )

    file_counted, df_counted = upload_csv_file(
        "Upload ytem app data (counted on Inventory Workflow)", col2
    )

# TEMP: upload directly from downloaded files
# df_expected = pd.read_csv("df-expected.csv", encoding="latin-1", na_values=["NaVal"])
# df_counted = pd.read_csv("df-counted.csv", encoding="latin-1", na_values=["NaVal"])

# If uploaded correctly, show dashboard
if df_expected is not None and df_counted is not None:
    file_readers.empty()
    discrepancy = get_discrepancy(df_expected, df_counted)

    # Create cols
    left, center = st.columns((1, 2))

    with left:
        # Change files section
        # left.subheader("Change files")
        # file_expected, df_expected = upload_csv_file(
        #     "Change customer data (expected Stock On Hand)", left, df_expected
        # )
        # file_expected, df_expected = upload_csv_file(
        #     "Change ytem app data (counted on Inventory Workflow)", left, df_counted
        # )

        # Statistics section
        left.subheader("Expected data CSV file info")
        left.markdown(get_statistics_as_markdown(file_expected, df_expected))

        left.subheader("Counted data CSV file info")
        left.markdown(get_statistics_as_markdown(file_counted, df_counted))

        left.subheader("Discrepancy DF info")
        left.markdown("DataFrame shape: {}".format(discrepancy.shape))
        left.write(discrepancy.isnull().sum().rename("Null values"))

    with center:
        center.subheader("Exploration by column")

        # Column selection
        options = ["Level1Name", "Level2Name", "Level3Name", "Color", "Size", "Style"]
        option = center.selectbox(
            "Pick a column to explore",
            list(map(lambda x: "Retail_Product_" + x, options)),
        )

        if option is None:
            option = "Retail_Product_Level1Name"

        # Statistics selection
        statistics = center.radio(
            "Select statistics to show", ["Unders", "Overs", "Both"], index=2
        )
        selected = []
        if statistics == "Both":
            selected = ["Unders", "Overs"]
        else:
            selected = [statistics]

        xlog = center.checkbox("Apply log scale to x-axis")

        # Plot
        fig, ax = plt.subplots(figsize=(16, 16))
        discrepancy.groupby(option).sum()[selected].sort_values(by=selected).plot.barh(
            ax=ax
        )
        ax.set_title("Amount of values with discrepancy on column {}".format(option))
        ax.set_xlabel(
            "Count of "
            + " and ".join(selected)
            + (" (log scale for clarity)" if xlog else "")
        )

        if xlog:
            ax.set_xscale("log")
        center.pyplot(fig)
