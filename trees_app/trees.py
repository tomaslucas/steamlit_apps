import streamlit as st
import pandas as pd

st.title('SF Trees')
st.write(
    """This app analyzes trees in San Francisco using a dataset kindly provided by SF DPW"""
)
trees_df = pd.read_csv('trees.csv')

trees_df = trees_df.dropna(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n = 1000)
st.map(trees_df)