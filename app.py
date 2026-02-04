import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績表示・フィルター", layout="wide")
st.title("⚾ 野球成績 フィルタリング表示")

# --- ファイルアップローダー ---
uploaded_file = st.file_uploader("エクセルファイル（.xlsx）を選択してください", type=["xlsx"])

def process_data(file):
    try:
        # 1. エクセル最上部の合計数値（5行目）を読み込む
        df_total_row = pd.read_excel(file, skiprows=4, nrows=1, dtype=str, header=None)
        
        # 2. 選手データ（見出しが6行目）を読み込む
        df_main = pd.read_excel(file, header=5, dtype=str)
        
        # 列名を合計行に合わせる
        df_total_row.columns = df_main.columns
        df_total_row.iloc[0, df_total_row.columns.get_loc('選手')] = '【合計】'
        if '球団' in df_total_row.columns:
            df_total_row.iloc[0, df_total_row.columns.get_loc('球団')] = 'ー'
        
        return df_main, df_total_row
    except Exception as e:
        st.error(f"解析エラー: {e}")
        return None, None

# --- メイン表示 ---
if uploaded_file is not None:
    df_main, df_total = process_data(uploaded_file)
    
    if df_main is not None:
        st.sidebar.header("🔍 フィルター設定")
        
        # 1. 球団フィルター
        all_teams = df_main['球団'].unique().tolist()
        selected_teams = st.sidebar.multiselect("球団を選択", all_teams, default=all_teams)
        
        # 2. 選手フィルター
        # 球団で絞り込まれた後の選手リストを出す
        temp_df = df_main[df_main['球団'].isin(selected_teams)]
        all_players = temp_df['選手'].unique().tolist()
        selected_players = st.sidebar.multiselect("選手を選択", all_players, default=all_players)

        # 3. 三振率フィルター（数値がある場合のみ）
        # 文字列を数値に変換してスライダーを作成
        if '三振率' in df_main.columns:
            df_main['三振率_num'] = pd.to_numeric(df_main['三振率'], errors='coerce').fillna(0)
            max_k_rate = float(df_main['三振率_num'].max())
            k_threshold = st.sidebar.slider("三振率の上限設定", 0.0, max_k_rate, max_k_rate)
            df_main = df_main[df_main['三振率_num'] <= k_threshold]

        # --- 絞り込み実行 ---
        df_filtered = df_main[
            (df_main['球団'].isin(selected_teams)) & 
            (df_main['選手'].isin(selected_players))
        ].copy()

        # --- 並べ替え（トヨタ優先・背番号順・理化さん下） ---
        df_toyota = df_filtered[df_filtered['球団'] == 'トヨタ'].copy()
        df_others = df_filtered[df_filtered['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
