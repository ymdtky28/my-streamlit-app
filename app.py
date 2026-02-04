import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# あなたがアップロードした実際のファイル名に修正しました
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(target):
        try:
            # トヨタのファイル形式に合わせて、6行目（header=5）から読み込みます
            df = pd.read_csv(target, encoding='utf-8', header=5)
            return df
        except:
            # 日本語の文字化け（Shift-JIS）対策
            try:
                df = pd.read_csv(target, encoding='cp932', header=5)
                return df
            except:
                return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    # 1列目の「選手名」などが正しく表示されるように表を出します
    st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
    st.info(f"GitHubにこの名前のファイルがあるか確認してください：\n{target}")
