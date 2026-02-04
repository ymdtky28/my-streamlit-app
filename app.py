import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 全列を「文字列」として読み込み、エクセルの見た目（6.70や合計値）を完全保護
            df = pd.read_excel(target, header=5, dtype=str)
            column_order = df.columns.tolist()
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    try:
        # 1. データを「選手」「理化」「合計行」に分ける
        # 選手列に「合計」が含まれる行を探す
        df_total = df[df['選手'].str.contains('合計', na=False)].copy()
        df_no_total = df[~df['選手'].str.contains('合計', na=False)].copy()
        
        # 理化さんとそれ以外（トヨタ等）に分ける
        df_rika = df_no_total[df_no_total['選手'].str.contains('理化', na=False)].copy()
        df_players = df_no_total[~df_no_total['選手'].str.contains('理化', na=False)].copy()

        # 2. 一般選手を背番号順に並べ替え
        df_players['sort_key'] = df_players['選手'].str.extract('(\d+)').astype(float)
        df_players = df_players.sort_values('sort_key').drop(columns=['sort_key'])

        # 3. 【トヨタ（背番号順）】→【理化】→【合計】の順で合体
        # これでプログラムの計算を挟まず、エクセルの合計行がそのまま出ます
        df_display = pd.concat([df_players, df_rika, df_total], ignore_index=True)

        # 4. 元の列順に整える
        display_cols = [c for c in original_cols if c in df_display.columns]
        df_display = df_display[display_cols]

        # 5. 書式設定
        format_dict = {}
        for col in df_display.columns:
            # 打率系だけは .300 形式を保証
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率（6.70など）や合計行の全数値をエクセルのまま表示
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("合計欄を含め、エクセルの数値をそのまま表示しています")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"表示エラー: {e}")
        st.dataframe(df)
