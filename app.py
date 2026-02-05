import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("トヨタ全打者成績一覧")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # 一旦すべて読み込む
        df = pd.read_csv(uploaded_file, encoding='cp932')
        
        # --- 「合計」より上をカットする処理 ---
        # 1列目（または全データ）の中に「合計」という文字がある行番号を探す
        mask = df.apply(lambda row: row.astype(str).str.contains('合計').any(), axis=1)
        
        if mask.any():
            # 「合計」が最初に見つかった行のインデックスを取得
            start_index = mask.idxmax()
            # その行から最後までを切り出す
            df = df.iloc[start_index:].reset_index(drop=True)
        # ---------------------------------------

        st.subheader("打撃成績表（合計以降）")
        st.dataframe(
            df, 
            use_container_width=True, 
            height=600,
            hide_index=True
        )
        
    except Exception as e:
        st.error(f"読み込みエラー: {e}")
else:
    st.info("CSVファイルをアップロードしてください。")
