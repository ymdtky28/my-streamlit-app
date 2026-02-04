import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 全列を文字列(str)として読み込み、エクセルの「.00」や「合計値」を完全に保護
            df = pd.read_excel(target, header=5, dtype=str)
            column_order = df.columns.tolist()
            
            # 日付での絞り込み用に内部で日付型を持つ
            if '日付' in df.columns:
                df['_date_internal'] = pd.to_datetime(df['日付'], errors='coerce')
                
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    # --- サイドバーでの絞り込み ---
    if '試合名' in df.columns:
        match_list = ['すべて'] + list(df['試合名'].dropna().unique())
        selected_match = st.sidebar.selectbox("試合名を選択", match_list)
        if selected_match != 'すべて':
            df = df[df['試合名'] == selected_match]

    try:
        # 1. データを「選手データ」と「合計行」に分離する
        # エクセルの「選手」列に「合計」が含まれる行を、計算せずそのまま保持
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()
        df_players_all = df[~df['選手'].str.contains('合計', na=False)].copy()

        # 2. 選手データを球団ごとに分ける
        df_toyota = df_players_all[df_players_all['球団'] == 'トヨタ'].copy()
        df_others = df_players_all[df_players_all['球団'] != 'トヨタ'].copy()

        # 3. グループ内並び替え（背番号順 ＋ 理化さんを末尾）
        def sort_group(target_df):
            if target_df.empty:
                return target_df
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号でソート
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        df_toyota_sorted = sort_group(df_toyota)
        df_others_sorted = sort_group(df_others)

        # 4. 【トヨタ】→【その他球団】→【エクセルの合計行】の順で結合
        # ここでプログラムによる sum() は一切行いません
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total], ignore_index=True)

        # 5. 元の列順に揃え、書式を適用
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        format_dict = {}
        for col in df_display.columns:
            # 打率などの「率」だけは .300 形式にするが、それ以外はエクセルの文字をそのまま出す
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率や、合計行のすべての数値にエクセルの見た目を適用
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("合計欄を含め、エクセルの数値をそのまま表示しています")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
