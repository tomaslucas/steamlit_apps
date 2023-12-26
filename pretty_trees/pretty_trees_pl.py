import streamlit as st
import polars as pl
from datetime import datetime
import plotly.express as px

st.set_page_config(layout='wide')
st.title("SF Trees")
st.write(
    """
    This app analyses trees in San Francisco using
    a dataset kindly provided by SF DPW.
    """
)
trees_df = pl.read_csv('trees.csv')
trees_df = trees_df.with_columns(
    age = (datetime.now() - pl.col('date').str.to_datetime()).dt.total_days()
)
unique_caretakers = trees_df.select("caretaker").unique(maintain_order=True).to_series()

owners = st.sidebar.multiselect("Tree Owner Filter", unique_caretakers)

if owners:
    trees_df = trees_df.filter(pl.col("caretaker").is_in(owners))

df_dbh_grouped = (trees_df
                  .group_by(pl.col('dbh'))
                  .agg(
                      pl.col('dbh').count().alias('tree_count')
                  )
                  .drop_nulls()
                  .sort('dbh')
                 )
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        trees_df, x='dbh',
        title="Tree Width")
    st.plotly_chart(fig)

with col2:
    fig = px.histogram(
        trees_df, x = 'age',
        title = 'Tree Age'
    )
    st.plotly_chart(fig)

st.write("Trees by Location")

trees_df = trees_df.drop_nulls(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n=1000, with_replacement=True)
st.map(trees_df)
