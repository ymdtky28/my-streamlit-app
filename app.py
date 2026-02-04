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
        # 1. 「トヨタ」のみに絞り込む
        df_toyota = df[df['球団'].str.contains('トヨタ', na=False)].copy()
        
        if not df_toyota.empty:
            # 2. 合計を計算する（数字の列だけを対象にする）
            # 出場数、打席、安打、本塁打、打点などの合計を出し、新しい行を作る
            numeric_cols = df_toyota.select_dtypes(include=['number']).columns
            total_values = df_toyota[numeric_cols].sum()
            
            # 3. 合計行をデータフレームの形式に整える
            total_df = pd.DataFrame(total_values).T
            total_df['選手'] = '【合計】'
            total_df['球団'] = 'トヨタ'
            
            # 4. 打率・出塁率などの「率」の項目は、単純合計ではなく計算し直す（任意）
            # もし単純合計でよければこのままでOKです。
            
            # 5. 元のデータと合計行を合体させる
            df_display = pd.concat([df_toyota, total_df], ignore_index=True)
            
            st.success("トヨタのデータを表示しています（一番下に合計を追加しました）")
            st.dataframe(df_display, use_container_width=True)
        else:
            st.warning("トヨタのデータが見つかりませんでした。")
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"計算エラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
