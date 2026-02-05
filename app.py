import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") # 画面を広く使って表を見やすくします
st.title("野球成績表 表示アプリ")

# 1. ファイルアップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # 日本語Excel系CSVに対応（encoding='cp932'）
        df = pd.read_csv(uploaded_file, encoding='cp932')
        
        # 2. 成績表の表示（シンプルに表だけ）
        st.subheader("打撃成績一覧")
        st.dataframe(df, use_container_width=True, height=600)
        
    except Exception as e:
        # エラーが出た場合は別の形式で試行
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            st.dataframe(df, use_container_width=True)
        except:
            st.error("ファイルの読み込みに失敗しました。CSV形式であることを確認してください。")
else:
    st.info("CSVファイルをアップロードしてください。")
