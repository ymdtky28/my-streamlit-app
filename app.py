import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="トヨタ野球部 成績一覧", layout="wide")

st.title("⚾ 野球成績一覧サイト")

# 1. データの読み込み
# CSVファイルを同じフォルダに置いておくか、GitHubにアップロードしておいてください
@st.cache_data
def load_data():
    # 最初の数行（タイトル部分）を飛ばして、5行目をヘッダーとして読み込む
    df = pd.read_csv("打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv", skiprow=4)
    # 不要な列や空の行があれば整理（必要に応じて調整）
    df = df.dropna(subset=['選手']) 
    return df

try:
    df = load_data()

    # 2. フィルタリング機能（サイドバー）
    st.sidebar.header("表示設定")
    search_name = st.sidebar.text_input("選手名で検索", "")
    
    # 選手名検索が入力されたら絞り込む
    if search_name:
        df = df[df['選手'].str.contains(search_name)]

    # 3. 成績の表示
    st.subheader("打撃成績表")
    
    # 表の表示（スクロール可能、並び替え可能）
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 4. 個別データ分析（おまけ）
    if not df.empty:
        st.divider()
        st.subheader("選手ピックアップ")
        selected_player = st.selectbox("詳細を見たい選手を選択", df['選手'].unique())
        
        player_stats = df[df['選手'] == selected_player].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("打率", player_stats['打率'])
        col2.metric("本塁打", player_stats['本塁打'])
        col3.metric("打点", player_stats['打点'])
        col4.metric("OPS（出塁+長打）", round(float(player_stats['長打率']) + float(player_stats['出塁率']), 3))

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
    st.info("CSVファイルが 'app.py' と同じフォルダにあるか確認してください。")
