import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 1. まず「合計」の数値が含まれる行（5行目）をピンポイントで読み込む
            df_total_row = pd.read_excel(target, skiprows=4, nrows=1, dtype=str, header=None)
            
            # 2. 次に、選手データ（見出しが6行目にある）を読み込む
            df_main = pd.read_excel(target, header=5, dtype=str)
            
            # 列名を合計行に適用
            df_total_row.columns = df_main.columns
            df_total_row['選手'] = '【合計】'
            df_total_row['球団'] = 'ー'
            
            column_order = df_main.columns.tolist()
            return df_main, df_total_row, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None, None
    return None, None, None

df, df_total, original_cols = load_data()

if df is not None:
    try:
        # --- 並び替えロジック ---
        # 選手データを「トヨタ（背番号順）」→「理化」の順に整理
        df_rika = df[df['選手'].str.contains('理化', na=False)].copy()
        df_players = df[~df['選手'].str.contains('理化', na=False)].copy()

        # 背番号順ソート
        df_players['sort_key'] = df_players['選手'].str.extract('(\d+)').astype(float)
        df_players = df_players.sort_values('sort_key').drop(columns=['sort_key'])

        # --- 最終結合 ---
        # 【トヨタ選手】→【理化さん】→【エクセル最上部にあった合計数値】
        df_display = pd.concat([df_players, df_rika, df_total], ignore_index=True)

        # 表示順をエクセルに合わせる
        df_display = df_display[original_cols]

        # --- 書式設定 ---
        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.
