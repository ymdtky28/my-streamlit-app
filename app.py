import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 全ての列を「文字列」として読み込み、Excelの見た目（8.00や合計値）を完全に保護します
            df = pd.read_excel(target, header=5, dtype=str)
            
            # 列の順番を記憶
            column_order = df.columns.tolist()
            
            # 日付列がある場合は、絞り込み用に日付型に変換（表示用とは別で保持）
            if '日付' in df.columns:
                df['_date_internal'] = pd.to_datetime(df['日付'], errors='coerce')
                
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    # --- サイドバー絞り込み ---
    if '試合名' in df.columns:
        match_list = ['すべて'] + list(df['試合名'].dropna().unique())
        selected_match = st.sidebar.selectbox("試合名を選択", match_list)
        if selected_match != 'すべて':
            df = df[df['試合名'] == selected_match]

    if '_date_internal' in df.columns:
        valid_dates = df['_date_internal'].dropna()
        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            date_range = st.sidebar.date_input("期間を選択", [min_date, max_date])
            if len(date_range) == 2:
                df = df[(df['_date_internal'].dt.date >= date_range[0]) & (df['_date_internal'].dt.date <= date_range[1])]

    try:
        # --- 表示用の処理 ---
        # 1. 背番号順に並べ替え（「【合計】」などの行は除外してソート）
        df_players = df[~df['選手'].str.contains('合計', na=False)].copy()
        df_players['sort_key'] = df_players['選手'].str.extract('(\d+)').astype(float)
        df_players = df_players.sort_values('sort_key').drop(columns=['sort_key'])
        
        # 2. Excel内の「合計」行を探して抽出する
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()
        
        # 3. 選手データとExcelの合計行を合体させる（プログラムで再計算しない）
        df_display = pd.concat([df_players, df_total], ignore_index=True)

        # 4. 不要な内部用列を削除し、元の列順に整える
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        # 5. 書式設定（打率系だけ野球形式にし、他はExcelの文字をそのまま出す）
        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                # これらもExcelの文字を優先するが、念のため数値変換して .300 形式を保証
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率や合計欄の数字など、全てExcelの打ち込みをそのまま表示
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("合計欄も含め、Excelの入力値をそのまま表示しています")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
