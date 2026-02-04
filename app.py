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
        total_df['球団'] = 'ー' # 球団名は空欄またはハイフンに
        
        # 3. 元の全データと合計行を合体させる
        df_all_with_total = pd.concat([df, total_df], ignore_index=True)
        
        st.success("全データを表示しています（一番下に全体の合計を追加しました）")
        
        # 4. 表を表示
        st.dataframe(df_all_with_total, use_container_width=True)
            
    except Exception as e:
        st.error(f"計算エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
