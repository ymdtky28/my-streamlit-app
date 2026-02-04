import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# 今GitHubにある正確なファイル名を指定します
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(target):
        try:
            # データの開始位置（6行目）に合わせて読み込みます
            df = pd.read_csv(target, encoding='utf-8', header=5)
            return df
        except:
            # 文字化け対策
            df = pd.read_csv(target, encoding='cp932', header=5)
            return df
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    # 表を表示
    st.dataframe(df, use_container_width=True)
else:
    st.error(f"ファイルが見つかりません: {target}")
    st.info("GitHubのトップ画面にファイルがあるか確認してください。")
