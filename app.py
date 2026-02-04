import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# ファイルの場所を指定（現在のGitHubの状態に合わせています）
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(target):
        try:
            # 5行目までがヘッダー情報なので、6行目から読み込む設定にしています
            df = pd.read_csv(target, encoding='cp932', skipfolders=0, header=5)
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    # データの表示
    st.dataframe(df, use_container_width=True)
else:
    st.error(f"ファイルが見つかりません: {target}")
    st.info("GitHubのトップ画面にファイルがあるか確認してください。")
