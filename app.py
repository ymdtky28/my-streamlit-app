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
        
        # 4. 特定の項目だけを野球形式（.300）にする設定
        # 他の項目（安打など）は、このリストに入れないことで「今まで通り」になります
        target_cols = ['打率', '長打率', '出塁率']
        format_dict = {}
        
        for col in target_cols:
            if col in df_all_with_total.columns:
                # 0.300 を .300 に書き換える命令
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""
        
        st.success("全データを表示しています（率は野球形式、その他は標準表示）")
        
        # 5. 表を表示（率の列だけに書式を適用し、他はそのまま）
        st.dataframe(df_all_with_total.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
