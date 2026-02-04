import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 【重要】三振率の列を読み込み段階で「文字列」として強制指定します
            df = pd.read_excel(target, header=5, dtype={'三振率': str})
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
    st.sidebar.header("絞り込み条件")
    if '試合名' in df.columns:
        match_list = ['すべて'] + list(df['試合名'].dropna().unique())
        selected_match = st.sidebar.selectbox("試合名を選択", match_list)
        if selected_match != 'すべて':
            df = df[df['試合名'] == selected_match]

    # --- 集計処理 ---
    try:
        # 計算が必要な数値列のみ抽出（三振率は文字列化したのでここには入りません）
        calc_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 選手・球団ごとに合計を計算
        df_sum = df.groupby(['選手', '球団'])[calc_cols].sum().reset_index()
        
        # 三振率は「最新の文字」をそのまま結合する
        if '三振率' in df.columns:
            so_rate_df = df.groupby(['選手', '球団'])['三振率'].last().reset_index()
            df_sum = pd.merge(df_sum, so_rate_df, on=['選手', '球団'], how='left')

        # 合計行の作成
        total_values = df_sum[calc_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー'
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # --- 表示フォーマットの適用 ---
        format_dict = {}
        for col in df_display.columns:
            # 1. 打率・長打率・出塁率・得点圏を野球形式 (.300) に
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' else ""
            
            # 2. 三振率は「文字列」としてそのまま表示（一切加工しない）
            elif col == '三振率':
                format_dict[col] = lambda x: str(x) if pd.notnull(x) else ""
            
            # 3. それ以外の数値列（安打、打席など）は整数表示
            elif col in calc_cols:
                format_dict[col] = "{:.0f}"
        
        st.success("三振率をExcelの文字列としてそのまま読み込みました")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラー: {e}")
        st.dataframe(df)
else:
    st.error("ファイルが見つかりません。")
