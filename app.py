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
        # 列名「球団」から「トヨタ」を含む行だけを抜き出す
        df_toyota = df[df['球団'].str.contains('トヨタ', na=False)]
        
        if not df_toyota.empty:
            st.success("トヨタのデータを表示しています")
            st.dataframe(df_toyota, use_container_width=True)
        else:
            # 万が一見つからない場合は、何が原因か探るために全データを表示
            st.warning("「トヨタ」に一致するデータが見つかりませんでした。")
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        # 「球団」という列が見つからない場合などのエラー対策
        st.info("全データを表示します。")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
