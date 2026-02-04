import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
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
        # 1. 全データを「一般選手」「理化」「合計」に分ける
        df_no_total = df[~df['選手'].str.contains('合計', na=False)].copy()
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()

        # 2. 一般選手の中で「トヨタ」と「それ以外」に分ける
        df_toyota = df_no_total[df_no_total['球団'] == 'トヨタ'].copy()
        df_others = df_no_total[df_no_total['球団'] != 'トヨタ'].copy()

        # 3. それぞれの中で「理化さん」を一番下にする処理
        def sort_and_extract_rika(target_df):
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号順にソート
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        # トヨタの選手（背番号順 + 理化）
        df_toyota_sorted = sort_and_extract_rika(df_toyota)
        # それ以外の球団の選手（背番号順 + 理化）
        df_others_sorted = sort_and_extract_rika(df_others)

        # 4. 【トヨタ】→【それ以外】→【合計】の順で合体
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total], ignore_index=True)

        # 5. 表示設定
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("球団トヨタを優先し、選手を並べ替えました")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
