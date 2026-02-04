import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            df = pd.read_excel(target, header=5)
            # 日付列がある場合、日付形式に変換
            if '日付' in df.columns:
                df['日付'] = pd.to_datetime(df['日付'])
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    # --- サイドバーで絞り込み設定 ---
    st.sidebar.header("絞り込み条件")
    
    # 1. 試合名で絞り込み
    if '試合名' in df.columns:
        match_list = ['すべて'] + list(df['試合名'].unique())
        selected_match = st.sidebar.selectbox("試合名を選択", match_list)
        if selected_match != 'すべて':
            df = df[df['試合名'] == selected_match]

    # 2. 期間で絞り込み
    if '日付' in df.columns:
        min_date = df['日付'].min().date()
        max_date = df['日付'].max().date()
        date_range = st.sidebar.date_input("期間を選択", [min_date, max_date])
        if len(date_range) == 2:
            df = df[(df['日付'].dt.date >= date_range[0]) & (df['日付'].dt.date <= date_range[1])]

    # --- 合計の計算と表示 ---
    try:
        # 数字列を抽出
        numeric_cols = df.select_dtypes(include=['number']).columns
        # 選手ごとに集計（蓄積データの場合、同じ選手を合算する）
        df_sum = df.groupby(['選手', '球団'])[numeric_cols].sum().reset_index()
        
        # 全体合計行の作成
        total_values = df_sum[numeric_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        
        # 最終表示用データ
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 書式設定
        format_dict = {col: "{:.0f}" for col in numeric_cols}
        rate_cols = ['打率', '長打率', '出塁率', '得点圏']
        for col in rate_cols:
            if col in df_display.columns:
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""

        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"計算エラー: {e}")
        st.dataframe(df)
else:
    st.error("ファイルが見つかりません。")
