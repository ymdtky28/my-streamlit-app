import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# ファイルの指定
target = 'data.csv'

def load_data():
    if os.path.exists(target):
        try:
            # 6行目 (header=5) から読み込みます
            df = pd.read_csv(target, encoding='utf-8', header=5)
            return df
        except:
            try:
                # 文字化け対策 (Shift-JIS)
                df = pd.read_csv(target, encoding='cp932', header=5)
                return df
            except:
                return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    st.dataframe(df) # 表を表示
else:
    st.error("ファイルが見つからないか、読み込めません。")
    st.write(f"GitHubに '{target}' があるか確認してください。")
