import pandas as pd
import streamlit as st
import os

def load_baseball_stats(file_path):
    # ファイルが存在するかまずチェック
    if not os.path.exists(file_path):
        st.error(f"ファイルが見つかりません: {file_path}")
        return None
    
    # 日本語のCSV（Excel書き出し）なら 'shift-jis' か 'cp932' が一般的
    try:
        return pd.read_csv(file_path, encoding='shift-jis')
    except:
        return pd.read_csv(file_path, encoding='utf-8')

# 実行
df_2025 = load_baseball_stats('data/成績表.xlsx - 2025.csv')

if df_2025 is not None:
    st.write(df_2025)
