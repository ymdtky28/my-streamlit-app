import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積システム", layout="wide")
st.title("⚾ 野球成績 蓄積・管理システム")

# 蓄積用データの保存先
DATA_FILE = "cumulative_data.csv"

def load_cumulative_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, dtype=str)
    return pd.DataFrame()

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- 1. 新しいエクセルを読み込んで蓄積する ---
st.sidebar.header("データ追加")
uploaded_file = st.sidebar.file_uploader("試合結果エクセルをアップ", type=["xlsx"])

if uploaded_file is not None:
    if st.sidebar.button("このデータを蓄積する"):
        try:
            # エクセルから選手データ（6行目以降）を読み込み
            new_df = pd.read_excel(uploaded_file, header=5, dtype=str)
            # 既存データと合体
            old_df = load_cumulative_data()
            combined_df = pd.concat([old_df, new_df], ignore_index=True).drop_duplicates()
            save_data(combined_df)
            st.sidebar.success("データを蓄積しました！")
        except Exception as e:
            st.sidebar.error(f"エラー: {e}")

# --- 2. 蓄積データの表示・計算 ---
df_all = load_cumulative_data()

if not df_all.empty:
    # 選手一覧の取得
    player_list = sorted(df_all['選手'].unique().tolist())
    selected_players = st.multiselect("表示する選手を選択", player_list, default=player_list)
    
    # 選択された選手で絞り込み
    df_filtered = df_all[df_all['選手'].isin(selected_players)].copy()

    # --- 数値計算（蓄積なので合計を出す） ---
    # 計算対象の列（安打、打数、本塁打など）を数値化
    calc_cols = [c for c in df_filtered.columns if c not in ['選手', '球団', '日付', '試合名', '三振率', '打率', '出塁率', '長打率']]
    for col in calc_cols:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0)

    # 選手ごとに合計を算出
    df_sum = df_filtered.groupby(['選手', '球団'])[calc_cols].sum().reset_index()

    # 打率などの率系を再計算（蓄積データから算出）
    def calc_stats(row):
        at_bats = row.get('打数', 0)
        hits = row.get('安打', 0)
        return hits / at_bats if at_bats > 0 else 0

    if '打数' in df_sum.columns and '安打' in df_sum.columns:
        df_sum['打率'] = df_sum.apply(calc_stats, axis=1)

    # --- 並び替え（トヨタ優先・理化・背番号順） ---
    df_toyota = df_sum[df_sum['球団'] == 'トヨタ'].copy()
    df_others = df_sum[df_sum['球団'] != 'トヨタ'].copy()

    def sort_group(target_df):
        if target_df.empty: return target_df
        rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
        others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
        others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
        others = others.sort_values('sort_key').drop(columns=['sort_key'])
        return pd.concat([others, rika], ignore_index=True)

    df_display = pd.concat([sort_group(df_toyota), sort_group(df_others)], ignore_index=True)

    # 合計行の追加
    total_row = df_display[calc_cols].sum().to_frame().T
    total_row['選手'] = '【合計】'
    total_row['球団'] = 'ー'
    df_final = pd.concat([df_display, total_row], ignore_index=True)

    # --- フォーマット表示 ---
    format_dict = {col: "{:.0f}" for col in calc_cols}
    if '打率' in df_final.columns:
        format_dict['打率'] = lambda x: f"{float(x):.3f}".replace("0.", ".") if x != 0 else ".000"

    st.dataframe(df_final.style.format(format_dict), use_container_width=True, hide_index=True)

    if st.button("蓄積データをリセットする"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()
else:
    st.info("左側のメニューからエクセルをアップロードして「蓄積」ボタンを押してください。")
