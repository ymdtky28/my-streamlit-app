import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="トヨタ野球成績", layout="wide")
st.title("⚾ トヨタ自動車 野球打撃成績")

# ファイルの指定
target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # Excelファイルを読み込み（6行目から）
            df = pd.read_excel(target, header=5)
            return df
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None
    return None

df = load_data()

if df is not None:
    try:
        # --- 1. 全体の合計値を計算（計算用） ---
        numeric_cols = df.select_dtypes(include=['number']).columns
        total_sum = df[numeric_cols].sum()
        
        # --- 2. 合計行の作成 ---
        total_df = pd.DataFrame(total_sum).T
        total_df['選手'] = '【全チーム合計】'
        total_df['球団'] = 'ー'

        # --- 3. 率の再計算（合計行のみ） ---
        # 打率 = 安打 / 打数
        if total_df.loc[0, '打数'] > 0:
            total_df.loc[0, '打率'] = total_df.loc[0, '安打'] / total_df.loc[0, '打数']
        
        # 出塁率 = (安打 + 四球 + 死球) / (打数 + 四球 + 死球 + 犠飛)
        on_base_den = total_df.loc[0, '打数'] + total_df.loc[0, '四球'] + total_df.loc[0, '死球'] + total_df.loc[0, '犠飛']
        if on_base_den > 0:
            total_df.loc[0, '出塁率'] = (total_df.loc[0, '安打'] + total_df.loc[0, '四球'] + total_df.loc[0, '死球']) / on_base_den
            
        # 長打率 = 塁打数 / 打数
        if total_df.loc[0, '打数'] > 0:
            total_df.loc[0, '長打率'] = total_df.loc[0, '塁打数'] / total_df.loc[0, '打数']

        # --- 4. データの合体 ---
        df_all = pd.concat([df, total_df], ignore_index=True)

        # --- 5. 見た目を「.333」形式に整える ---
        # 対象の列を小数点第3位で表示するように設定
        rate_cols = ['打率', '長打率', '出塁率']
        format_dict = {col: "{:.3f}" for col in rate_cols}
        
        st.success("全データを表示しています（率は計算し直しています）")
        
        # 表示（formatを使って小数点以下を固定）
        st.dataframe(df_all.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
