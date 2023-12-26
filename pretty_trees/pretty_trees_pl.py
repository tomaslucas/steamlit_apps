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

# first_width = st.number_input('First Width', min_value=1, value=1)
# second_width = st.number_input('Second Width', min_value=1, value=1)
# third_width = st.number_input('Third Width', min_value=1, value=1)
# col1, col2, col3 = st.columns(
#       (first_width,second_width,third_width))

col1, col2, col3 = st.columns(3, gap='large')

with col1:
    st.line_chart(df_dbh_grouped, x='dbh', y='tree_count')
with col2:
    st.bar_chart(df_dbh_grouped, x='dbh', y='tree_count')
with col3:
    st.area_chart(df_dbh_grouped, x='dbh', y='tree_count')