import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績表示システム", layout="wide")
st.title("⚾ 野球成績 選手別表示")

# --- ファイルアップローダー ---
uploaded_file = st.file_uploader("エクセルファイルをアップロードしてください", type=["xlsx"])

def process_data(file):
    try:
        # 1. エクセル最上部の合計行（5行目）を読み込む
        df_total_row = pd.read_excel(file, skiprows=4, nrows=1, dtype=str, header=None)
        
        # 2. 選手データ（見出しが6行目にある）を読み込む
        df_main = pd.read_excel(file, header=5, dtype=str)
        
        # 列名を合計行に適用
        df_total_row.columns = df_main.columns
        df_total_row['選手'] = '【合計】'
        df_total_row['球団'] = 'ー'
        
        original_cols = df_main.columns.tolist()
        
        # --- 並び替えとフィルタリングの準備 ---
        df_no_total = df_main[~df_main['選手'].str.contains('合計', na=False)].copy()
        
        # サイドバーで選手を選択（デフォルトは全員）
        player_list = df_no_total['選手'].unique().tolist()
        selected_players = st.sidebar.multiselect("表示する選手を選択してください", player_list, default=player_list)
        
        # 選択された選手だけで絞り込み
        df_filtered = df_no_total[df_no_total['選手'].isin(selected_players)].copy()

        # トヨタとそれ以外に分けてソート
        df_toyota = df_filtered[df_filtered['球団'] == 'トヨタ'].copy()
        df_others = df_filtered[df_filtered['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
            if target_df.empty: return target_df
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        df_toyota_sorted = sort_group(df_toyota)
        df_others_sorted = sort_group(df_others)

        # 最終結合（選んだ選手たち -> エクセルの合計）
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total_row], ignore_index=True)
        df_display = df_display[original_cols]

        return df_display
    except Exception as e:
        st.error(f"解析エラー
