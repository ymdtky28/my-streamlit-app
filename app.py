import streamlit as st
import pandas as pd
import os

# --- 1. 関数を「定義」する（必ず呼び出しより上に書く） ---
def load_baseball_stats(file_path):
    # ファイルが存在するか確認
    if not os.path.exists(file_path):
        st.error(f"ファイルが見つかりません: {file_path}")
        return None
    
    # 日本語のCSV（Excel書き出し）に対応するための設定
    try:
        # ExcelからのCSVは 'cp932' という形式が多いです
        df = pd.read_csv(file_path, encoding='cp932')
    except:
        # ダメなら一般的な 'utf-8' で試す
        df = pd.read_csv(file_path, encoding='utf-8')
    
    return df

# --- 2. メインの処理（ここで関数を呼び出す） ---
st.title("野球成績一覧")

# ファイルパスを指定（dataフォルダの中にあることを確認してください）
file_path_2025 = 'data/成績表.xlsx - 2025.csv'

# 関数を使ってデータを読み込む
df_2025 = load_baseball_stats(file_path_2025)

# 読み込みに成功したら表示する
if df_2025 is not None:
    st.success("2025年のデータを読み込みました")
    st.dataframe(df_2025)
