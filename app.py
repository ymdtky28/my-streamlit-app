import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# あなたがアップロードした実際のファイル名に修正しました
# 修正前
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

# 修正後（フォルダ名の "date/" を最初に追加します）
target = 'date/打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'
