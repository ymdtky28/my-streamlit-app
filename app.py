import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# あなたがアップロードした最新のファイル名に正確に合わせました
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(target):
        try:
            # トヨタのファイルは5行目までがタイトル等なので、6行目（header=5）から読み込みます
            df = pd.read_csv(target, encoding='utf-8', header=5)
            return df
        except:
            # 日本語が文字化けする場合の対策
            try:
                df = pd.read_csv(target, encoding='cp932', header=5)
                return df
            except:
                return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    # 数値列をきれいに表示
    st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
    st.info(f"確認：GitHubのトップに '{target}' があるか見てください。")
