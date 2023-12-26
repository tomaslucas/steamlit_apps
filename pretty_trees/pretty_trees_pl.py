import streamlit as st
import polars as pl

st.set_page_config(layout='wide')
st.title("SF Trees")
st.write(
    """
    This app analyses trees in San Francisco using
    a dataset kindly provided by SF DPW.
    """
)
trees_df = pl.read_csv('trees.csv')

owners = st.sidebar.multiselect("Tree Owner Filter", trees_df.select("caretaker").unique(maintain_order=True).to_series())
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

st.line_chart(df_dbh_grouped, x='dbh', y='tree_count')

trees_df = trees_df.drop_nulls(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n=1000, with_replacement=True)
st.map(trees_df)
