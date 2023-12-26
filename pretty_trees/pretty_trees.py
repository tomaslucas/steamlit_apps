import streamlit as st
import pandas as pd
st.set_page_config(layout='wide')
st.title("SF Trees")
st.write(
    """
    This app analyses trees in San Francisco using
    a dataset kindly provided by SF DPW.
    """
)
trees_df = pd.read_csv('trees.csv')
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['tree_count']

# first_width = st.number_input('First Width', min_value=1, value=1)
# second_width = st.number_input('Second Width', min_value=1, value=1)
# third_width = st.number_input('Third Width', min_value=1, value=1)
# col1, col2, col3 = st.columns(
#       (first_width,second_width,third_width))

col1, col2, col3 = st.columns(3, gap='large')

with col1:
    st.line_chart(df_dbh_grouped)
with col2:
    st.bar_chart(df_dbh_grouped)
with col3:
    st.area_chart(df_dbh_grouped)