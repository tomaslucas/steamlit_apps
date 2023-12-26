import polars as pl
import streamlit as st
st.title("SF Trees Data Quality App")
st.write(
    """This app is a data quality tool for the SF trees dataset. Edit the data and save to a new file!"""
)
trees_df = pl.read_csv("trees.csv").drop_nulls(subset=['longitude', 'latitude'])
trees_df_filtered = trees_df.filter(pl.col('legal_status') == "Private").to_arrow()
edited_df = st.data_editor(trees_df_filtered)
edited_df = pl.from_arrow(edited_df)
#trees_df = 
trees_df = trees_df.update(edited_df, on=['tree_id'], how='outer')
if st.button("Save data and overwrite:"):
    trees_df.write_csv("trees.csv")
    st.write("Saved!")