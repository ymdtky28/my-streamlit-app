import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="トヨタ野球部 成績管理", layout="wide")

st.title("⚾ 野球成績アップロード・閲覧サイト")

# サイドバーでファイルをアップロード（xlsxに対応）
st.sidebar.header("データ読み込み")
uploaded_file = st.sidebar.file_uploader("成績表（Excel）を選択してください", type=["xlsx"])

def load_data(file):
    # Excelファイルを読み込む。5行目をヘッダーとする（skiprows=5）
    # engine='openpyxl' を指定してExcel形式に対応させる
    df = pd.read_excel(file, skiprows=5, engine='openpyxl')
    
    # 「選手」列が空の行を削除（データの終わり以降の空行対策）
    df = df.dropna(subset=['選手'])
    return df

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        
        # 選手検索機能
        search_name = st.sidebar.text_input("選手名で検索", "")
        if search_name:
            df = df[df['選手'].str.contains(search_name)]

        st.success(f"Excelファイル「{uploaded_file.name}」を読み込みました")
        
        st.subheader("📊 打撃成績一覧")
        # 数値データが変な形式にならないよう調整して表示
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 個別分析
        st.divider()
        st.subheader("👤 選手ピックアップ")
        unique_players = df['選手'].unique()
        selected_player = st.selectbox("詳細を見たい選手を選択", unique_players)
        
        player_stats = df[df['選手'] == selected_player].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("打率", f"{player_stats['打率']:.3f}" if isinstance(player_stats['打率'], float) else player_stats['打率'])
        col2.metric("安打", int(player_stats['安打']))
        col3.metric("本塁打", int(player_stats['本塁打']))
        col4.metric("打点", int(player_stats['打点']))

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info("Excelのフォーマットが正しいか確認してください（5行目までタイトル、6行目からヘッダーを想定）。")
else:
    st.info("左側のサイドバーからExcelファイル（.xlsx）をアップロードしてください。")
