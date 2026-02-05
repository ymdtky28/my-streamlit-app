import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("トヨタ全打者成績一覧")

# ファイルアップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # 日本語Excel系CSVに対応
        df = pd.read_csv(uploaded_file, encoding='cp932')
        
        # 0, 1, 2... の行番号を消して表示
        st.subheader("打撃成績表")
        st.dataframe(
            df, 
            use_container_width=True, 
            height=600,
            hide_index=True  # ← これで左端の番号が消えます
        )
        
    except Exception:
        # 文字コードが違う場合の再試行
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("CSVファイルをアップロードしてください。")
