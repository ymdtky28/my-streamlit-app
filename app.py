import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 【ポイント】読み込み時に「三振率」を文字として扱うように指定
            df = pd.read_excel(target, header=5)
            if '三振率' in df.columns:
                df['三振率'] = df['三振率'].astype(str)
            if '日付' in df.columns:
                df['日付'] = pd.to_datetime(df['日付'])
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    # --- サイドバー絞り込み ---
    # (既存の絞り込みコード)
    
    try:
        # 計算用（数値）と表示用（文字）を分ける
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 選手ごとに集計（数値列のみ）
        df_sum = df.groupby(['選手', '球団'])[numeric_cols].sum().reset_index()
        
        # 三振率は「最新の文字」をそのまま持ってくる
        if '三振率' in df.columns:
            so_rate_df = df.groupby(['選手', '球団'])['三振率'].last().reset_index()
            df_sum = pd.merge(df_sum, so_rate_df, on=['選手', '球団'], how='left')

        # 合計行
        total_values = df_sum[numeric_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー'
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # --- 表示設定（ここが重要） ---
        format_dict = {}
        for col in df_display.columns:
            # 1. 三振率は「加工せずそのまま」の文字を出す
            if col == '三振率':
                format_dict[col] = lambda x: x if pd.notnull(x) else ""
            
            # 2. 打率などは「.300」形式
            elif col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) else ""
            
            # 3. その他は整数
            elif col in numeric_cols:
                format_dict[col] = "{:.0f}"

        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラー: {e}")
        st.dataframe(df)
