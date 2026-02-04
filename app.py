import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# GitHubにある実際のファイル名に合わせました
target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # Excelファイルとして読み込みます（6行目から）
            df = pd.read_excel(target, header=5)
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    st.dataframe(df)
else:
    st.error("ファイルが見つかりません。")
    st.write(f"GitHubに '{target}' があるか確認してください。")
