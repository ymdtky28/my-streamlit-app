import streamlit as st
import pandas as pd

# 1. Define the function FIRST
def load_baseball_stats(file_path):
    return pd.read_csv(file_path)

# 2. Then call the function
df_2025 = load_baseball_stats('data/成績表.xlsx - 2025.csv')

st.write(df_2025)
