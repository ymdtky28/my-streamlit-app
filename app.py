import streamlit as st
import pandas as pd

# 関数の定義
def sort_group(target_df):
    # もし「打率」という列があれば、それで並び替える
    if "打率" in target_df.columns:
        return target_df.sort_values(by="打率", ascending=False)
    return target_df

st.title("トヨタ全打者成績分析")

# ファイルアップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # 日本語のExcel系CSVに対応するために encoding='cp932' を指定
        df = pd.read_csv(uploaded_file, encoding='cp932')
        
        # データの表示
        st.success("読み込みに成功しました！")
        
        # 並び替え関数の呼び出し
        sorted_df = sort_group(df)
        
        # 表を表示
        st.write("### 成績一覧")
        st.dataframe(sorted_df)

    except Exception as e:
        # もし上の読み込みでエラーが出た場合の予備（別の文字コードで試す）
        try:
            uploaded_file.seek(0) # 読み込み位置を最初に戻す
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            st.dataframe(df)
        except Exception as e2:
            st.error(f"エラーが発生しました: {e2}")
else:
    st.info("左側のボタン、またはここにファイルをドラッグ＆ドロップしてください。")
