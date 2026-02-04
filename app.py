import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# あなたがアップロードした最新のファイル名に合わせました
target = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(target):
        try:
            # データの開始位置（6行目）に合わせて読み込みます
            # トヨタのファイルはヘッダーが特殊なので header=5 に設定しています
            df = pd.read_csv(target, encoding='utf-8', header=5)
            return df
        except:
            # 文字化け対策（Shift-JISの場合）
            try:
                df = pd.read_csv(target, encoding='cp932', header=5)
                return df
            except:
                return None
    return None

df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    # 表を表示
    st.dataframe(df, use_container_width=True)
else:
    st.error(f"ファイルが見つかりません。")
    st.info(f"現在探している名前: {target}")
    # デバッグ用：今GitHubにあるファイルを表示
    st.write("GitHubにあるファイル一覧:", os.listdir('.'))
