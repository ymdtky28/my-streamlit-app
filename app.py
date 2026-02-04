import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 1. 読み込みの瞬間、三振率を「文字列（str）」として固定。これで 8.00 が維持されます。
            df = pd.read_excel(target, header=5, dtype={'三振率': str})
            
            # 2. 三振率以外の数字列を計算用に変換
            numeric_cols = [c for c in df.columns if c not in ['選手', '球団', '日付', '試合名', '三振率']]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            if '日付' in df.columns:
                df['日付'] = pd.to_datetime(df['日付'])
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    # --- 絞り込み処理などは既存のままでOK ---
    
    try:
        calc_cols = df.select_dtypes(include=['number']).columns.tolist()
        df_sum = df.groupby(['選手', '球団'])[calc_cols].sum().reset_index()
        
        # 3. 三振率（文字データ）を、計算後の表に合体させる
        if '三振率' in df.columns:
            so_rate_df = df.groupby(['選手', '球団'])['三振率'].last().reset_index()
            df_sum = pd.merge(df_sum, so_rate_df, on=['選手', '球団'], how='left')

        total_values = df_sum[calc_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー'
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 4. 【ここが最重要】表示の瞬間に「三振率はそのまま出せ」と命令
        format_dict = {}
        for col in df_display.columns:
            if col == '三振率':
                # 文字列としてそのまま表示。絶対に数字に変換させない
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""
            elif col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and str(x) != 'nan' else ""
            elif col in calc_cols:
                format_dict[col] = "{:.0f}"

        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラー: {e}")
        st.dataframe(df)
