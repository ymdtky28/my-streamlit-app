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
    # --- ここから「トヨタ」に絞り込む処理 ---
    # 「チーム」という名前の列から「トヨタ自動車」を探します
    # ※列名が「チーム」でない場合は、エラーが出ないよう処理します
    try:
        # チーム名に「トヨタ」を含む行だけを抜き出す
        df_toyota = df[df['チーム'].str.contains('トヨタ', na=False)]
        
        if not df_toyota.empty:
            st.success("トヨタ自動車のデータを表示しています")
            st.dataframe(df_toyota, use_container_width=True)
        else:
            st.warning("「トヨタ」に一致するデータが見つかりませんでした。全データを表示します。")
            st.dataframe(df, use_container_width=True)
            
    except Exception:
        # 万が一「チーム」という列名が違った場合は、全てのデータを表示
        st.info("フィルタリングなしで全データを表示します。")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
