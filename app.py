import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 1. まず全データを「文字列」として読み込む（勝手な数字変換を防ぐ）
            df_raw = pd.read_excel(target, header=5, dtype=str)
            
            # 2. 計算に必要な列だけ数値に戻す
            df = df_raw.copy()
            numeric_cols = [c for c in df.columns if c not in ['選手', '球団', '日付', '試合名', '三振率']]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 3. 日付を変換
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
    # (既存のコードがあればそのまま)

    try:
        # 数値列のリスト（三振率は含めない）
        calc_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 集計
        df_sum = df.groupby(['選手', '球団'])[calc_cols].sum().reset_index()
        
        # 三振率は「Excelの生データ」をそのまま結合（計算しない）
        if '三振率' in df.columns:
            so_rate_df = df.groupby(['選手', '球団'])['三振率'].last().reset_index()
            df_sum = pd.merge(df_sum, so_rate_df, on=['選手', '球団'], how='left')

        # 合計行
        total_values = df_sum[calc_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー'
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # --- 表示設定 ---
        format_dict = {}
        for col in df_display.columns:
            # 三振率は一切加工せず、読み込んだ文字（8.00等）をそのまま出す
            if col == '三振率':
                format_dict[col] = lambda x: x if pd.notnull(x) and x != 'nan' else ""
            
            # 率の項目は野球形式
            elif col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and str(x) != 'nan' else ""
            
            # その他は整数
            elif col in calc_cols:
                format_dict[col] = "{:.0f}"

        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラー: {e}")
        st.dataframe(df)
