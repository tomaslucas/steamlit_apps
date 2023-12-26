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
df_dbh_grouped = (trees_df
                  .group_by(pl.col('dbh'))
                  .agg(
                      pl.col('dbh').count().alias('tree_count')
                  )
                  .drop_nulls()
                  .sort('dbh')
                 )

tab1, tab2, tab3 = st.tabs(["Line Chart", "Bar Chart", "Area Chart"])

with tab1:
    st.line_chart(df_dbh_grouped, x='dbh', y='tree_count')
with tab2:
    st.bar_chart(df_dbh_grouped, x='dbh', y='tree_count')
with tab3:
    st.area_chart(df_dbh_grouped, x='dbh', y='tree_count')