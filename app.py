import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績表示", layout="wide")
st.title("⚾ 野球成績 エクセルアップロード表示")

# --- ファイルアップローダーの設置 ---
uploaded_file = st.file_uploader("エクセルファイル（.xlsx）を選んでください", type=["xlsx"])

def process_data(file):
    try:
        # 1. エクセルの5行目（skiprows=4）にある合計値を読み込む
        # header=Noneで読み込み、後で列名を合わせる
        df_total_row = pd.read_excel(file, skiprows=4, nrows=1, dtype=str, header=None)
        
        # 2. 選手データ（6行目が見出し）を読み込む
        df_main = pd.read_excel(file, header=5, dtype=str)
        
        # 合計行の列名をメインデータと一致させる
        df_total_row.columns = df_main.columns
        df_total_row['選手'] = '【合計】'
        df_total_row['球団'] = 'ー'
        
        original_cols = df_main.columns.tolist()
        
        # --- 並べ替えロジック ---
        # 「合計」という文字を含む行があれば除外（念のため）
        df_no_total = df_main[~df_main['選手'].str.contains('合計', na=False)].copy()
        
        # トヨタとそれ以外に分離
        df_toyota = df_no_total[df_no_total['球団'] == 'トヨタ'].copy()
        df_others = df_no_total[df_no_total['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
            if target_df.empty: return target_df
            # 理化さんを抜き出す
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号順（数字抽出）でソート
            others['sort_
