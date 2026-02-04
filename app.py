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
        # 1. 数字の列だけを抽出して合計を計算
        numeric_cols = df.select_dtypes(include=['number']).columns
        total_values = df[numeric_cols].sum()
        
        # 2. 合計行を作成
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【全チーム合計】'
        total_df['球団'] = 'ー'
        
        # 3. 元の全データと合計行を合体させる
        df_all_with_total = pd.concat([df, total_df], ignore_index=True)
        
        # 4. 列ごとの表示形式を設定
        format_dict = {}
        
        # 全ての数字列を一旦「整数」にする設定（小数点以下を非表示）
        for col in numeric_cols:
            format_dict[col] = "{:.0f}"
            
        # 打率・長打率・出塁率だけ「.300」形式で上書き
        rate_cols = ['打率', '長打率', '出塁率']
        for col in rate_cols:
            if col in df_all_with_total.columns:
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""
        
        st.success("全データを表示しています（率は野球形式、他は整数表示）")
        
        # 5. 表を表示
        st.dataframe(df_all_with_total.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
