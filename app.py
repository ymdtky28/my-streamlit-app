import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# あなたがアップロードした実際のファイル名に修正しました
# ファイルの指定
target = 'data.csv'
