import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績表示", layout="wide")
st.title("⚾ 野球成績 エクセルアップロード")

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
        
        original_cols = df_main.columns.tolist()
        
        # --- 並べ替え ---
        df_no_total = df_main[~df_main['選手'].str.contains('合計', na=False)].copy()
        df_toyota = df_no_total[df_no_total['球団'] == 'トヨタ'].copy()
        df_others = df_no_total[df_no_total['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
            if target_df.empty: return target_df
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        df_display = pd.concat([sort_group(df_toyota), sort_group(df_others), df_total_row], ignore_index=True)
        return df_display[original_cols]
    except Exception as e:
        st.error(f"解析エラー: {e}")
        return None

# --- メイン表示 ---
if uploaded_file is not None:
    df_result = process_data(uploaded_file)
    
    if df_result is not None:
        # 選手選択フィルター
        player_list = df_result[df_result['選手'] != '【合計】']['選手'].unique().tolist()
        selected = st.sidebar.multiselect("表示する選手を選択", player_list)
        
        display_final = df_result.copy()
        if selected:
            display_final = df_result[df_result['選手'].isin(selected) | (df_result['選手'] == '【合計】')]

        # --- 書式設定（エラー対策強化版） ---
        def format_stats(val):
            if pd.isnull(val) or str(val).strip() in ['', 'nan', 'ー', '-']:
                return str(val) if pd.notnull(val) else ""
            try:
                # 数字に変換できる場合だけ .300 形式にする
                num = float(val)
                return f"{num:.3f}".replace("0.", ".")
            except:
                # 数字にできない文字（「ー」など）ならそのまま出す
                return str(val)

        format_dict = {}
        for col in display_final.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = format_stats
            else:
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("アップロード完了！")
        st.dataframe(display_final.style.format(format_dict), use_container_width=True, hide_index=True)
