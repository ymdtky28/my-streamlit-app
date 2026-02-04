import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 全列を文字列として読み込み、エクセルの書式（8.00など）を完全保護
            df = pd.read_excel(target, header=5, dtype=str)
            column_order = df.columns.tolist()
            if '日付' in df.columns:
                df['_date_internal'] = pd.to_datetime(df['日付'], errors='coerce')
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    # --- サイドバー処理（省略） ---

    try:
        # 1. 選手データを「一般選手」「理化」「合計」の3グループに分ける
        # 合計行を除外
        df_no_total = df[~df['選手'].str.contains('合計', na=False)].copy()
        
        # 理化さんの行を分離
        df_rika = df_no_total[df_no_total['選手'].str.contains('理化', na=False)].copy()
        # 理化さん以外の一般選手
        df_players = df_no_total[~df_no_total['選手'].str.contains('理化', na=False)].copy()
        
        # 2. 一般選手を背番号順に並べ替え
        df_players['sort_key'] = df_players['選手'].str.extract('(\d+)').astype(float)
        df_players = df_players.sort_values('sort_key').drop(columns=['sort_key'])
        
        # 3. エクセル内の「合計」行を抽出
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()
        
        # 4. 【一般選手】→【理化】→【合計】の順番で合体させる
        df_display = pd.concat([df_players, df_rika, df_total], ignore_index=True)

        # 5. 列順を整え、書式を適用
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率や合計の数字もエクセルのまま表示
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("選手を背番号順、理化さんと合計を一番下に配置しました")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
