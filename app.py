import streamlit as st
import pandas as pd

# 関数の定義（エラーの箇所）
def sort_group(target_df):
    # ここでインデント（半角スペース4つ）を入れて処理を書きます
    # 例：打率が高い順に並び替える
    if '打率' in target_df.columns:
        return target_df.sort_values(by='打率', ascending=False)
    else:
        return target_df

st.title("打撃成績分析アプリ")

# ファイルの読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 関数の呼び出し
    st.subheader("分析結果")
    sorted_df = sort_group(df)
    st.dataframe(sorted_df)
    
