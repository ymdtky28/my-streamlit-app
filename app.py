import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="トヨタ野球部 成績管理", layout="wide")

st.title("⚾ 野球成績アップロード・閲覧サイト")

# サイドバーでファイルをアップロード
st.sidebar.header("データ読み込み")
uploaded_file = st.sidebar.file_uploader("成績表（CSV）を選択してください", type=["csv"])

def load_data(file):
    # 5行目をヘッダーとして読み込む（提供されたフォーマットに合わせる）
    df = pd.read_csv(file, skiprows=5)
    # 選手名が空の行を削除
    df = df.dropna(subset=['選手'])
    return df

if uploaded_file is not None:
    # ファイルがアップロードされた場合
    try:
        df = load_data(uploaded_file)
        
        # 選手検索機能
        search_name = st.sidebar.text_input("選手名で検索", "")
        if search_name:
            df = df[df['選手'].str.contains(search_name)]

        # メイン画面の表示
        st.success(f"ファイル「{uploaded_file.name}」を読み込みました")
        
        st.subheader("📊 打撃成績一覧")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 個別分析
        st.divider()
        st.subheader("👤 選手ピックアップ")
        selected_player = st.selectbox("詳細を見たい選手を選択", df['選手'].unique())
        
        player_stats = df[df['選手'] == selected_player].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("打率", player_stats['打率'])
        col2.metric("安打", int(player_stats['安打']))
        col3.metric("本塁打", int(player_stats['本塁打']))
        col4.metric("打点", int(player_stats['打点']))

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    # ファイルがまだアップロードされていない時
    st.info("左側のサイドバーからCSVファイルをアップロードしてください。")
    st.image("https://via.placeholder.com/800x400.png?text=Please+Upload+CSV+File") # 代替イメージ
