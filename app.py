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
        
        # 4. 「.300」形式（頭の0を消して小数点第3位まで）にする設定
        # 対象：打率、長打率、出塁率
        format_dict = {}
        for col in ['打率', '長打率', '出塁率']:
            if col in df_all_with_total.columns:
                # 0.3333... を ".333" に変換する命令
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""
        
        st.success("全データを表示しています（野球形式の表示に整えました）")
        
        # 5. 表を表示（作成した書式を適用）
        st.dataframe(df_all_with_total.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
