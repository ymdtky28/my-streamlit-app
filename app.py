import streamlit as st
import pandas as pd
import os

st.title("野球成績チェック")

# 読み込み関数
def load_data():
    # フォルダ名に合わせて 'date/' にしています
    target = 'date/成績表.xlsx - 2025.csv'
    
    if os.path.exists(target):
        try:
            return pd.read_csv(target, encoding='cp932')
        except:
            return pd.read_csv(target, encoding='utf-8')
    return None

# 実行
df = load_data()

if df is not None:
    st.success("データの読み込みに成功しました！")
    st.dataframe(df)
else:
    st.error("ファイルが見つかりません。GitHubのフォルダ名が 'date' になっているか確認してください。")
    # デバッグ用：今あるフォルダを表示
    st.write("現在のフォルダ一覧:", os.listdir('.'))
    if os.path.exists('date'):
        st.write("dateフォルダの中身:", os.listdir('date'))
