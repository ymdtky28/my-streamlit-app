import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 全列を文字列(str)として読み込み、エクセルの「.00」や合計値を完全保護
            df = pd.read_excel(target, header=5, dtype=str)
            column_order = df.columns.tolist()
            
            # 絞り込み用に内部で日付型を持つ
            if '日付' in df.columns:
                df['_date_internal'] = pd.to_datetime(df['日付'], errors='coerce')
                
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    # --- サイドバー処理（既存の絞り込み） ---
    if '試合名' in df.columns:
        match_list = ['すべて'] + list(df['試合名'].dropna().unique())
        selected_match = st.sidebar.selectbox("試合名を選択", match_list)
        if selected_match != 'すべて':
            df = df[df['試合名'] == selected_match]

    try:
        # 1. データを「選手データ」と「合計行」に分ける
        # エクセルの「選手」列に「合計」という文字がある行を「合計行」として扱う
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()
        df_players_all = df[~df['選手'].str.contains('合計', na=False)].copy()

        # 2. 選手データを「トヨタ」と「その他」に分ける
        df_toyota = df_players_all[df_players_all['球団'] == 'トヨタ'].copy()
        df_others = df_players_all[df_players_all['球団'] != 'トヨタ'].copy()

        # 3. 各グループ内で「背番号順」にしつつ「理化」さんを末尾にする関数
        def sort_group(target_df):
            if target_df.empty:
                return target_df
            # 理化さんを分離
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号（#以降の数字）でソート
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        # 並び替え実行
        df_toyota_sorted = sort_group(df_toyota)
        df_others_sorted = sort_group(df_others)

        # 4. 【トヨタ】→【その他】→【エクセルの合計】の順で最終合体
        # これでプログラムによる計算(sum)を一切介さず、エクセルの数字がそのまま並びます
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total], ignore_index=True)

        # 5. 表示列の整理と書式適用
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                # 率の項目は .300 形式を維持（エクセルが 0.3 の場合でも対応）
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率や合計行の数値など、エクセルの入力をそのまま表示
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("エクセルの数値をそのまま、指定の順序で表示しました")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
