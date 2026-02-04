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
        # 「球団」列が「トヨタ」のデータだけを表示
        df_toyota = df[df['球団'].str.contains('トヨタ', na=False)]
        
        if not df_toyota.empty:
            st.success("トヨタのデータを表示しています")
            
            # --- 合計の計算 ---
            # 合計を出したい数値列（出場数から出塁率の前まで）を指定します
            # ※ df_toyota.select_dtypes(include='number') を使うと数字の列だけ自動で選べます
            numeric_df = df_toyota.select_dtypes(include='number')
            total_row = numeric_df.sum().to_frame().T
            total_row['選手'] = '【合計】'
            total_row['球団'] = 'トヨタ'
            
            # 元の表と合計行を合体させる
            df_with_total = pd.concat([df_toyota, total_row], ignore_index=True)
            
            # 表を表示
            st.dataframe(df_with_total, use_container_width=True)
            
            # --- 別の見せ方：重要な指標の合計をカードで表示 ---
            st.subheader("📊 チーム合計（主要項目）")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("総安打数", int(numeric_df['安打'].sum()))
            col2.metric("総本塁打", int(numeric_df['本塁打'].sum()))
            col3.metric("総打点", int(numeric_df['打点'].sum()))
            col4.metric("総四死球", int(numeric_df['四球'].sum() + numeric_df['死球'].sum()))

        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"合計の計算中にエラーが発生しました: {e}")
        st.dataframe(df, use_container_width=True)
else:
    st.error("ファイルが見つかりません。")
