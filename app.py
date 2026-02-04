import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績表示", layout="wide")
st.title("⚾ 野球成績 エクセルアップロード")

# --- ファイルアップローダーの設置 ---
uploaded_file = st.file_uploader("エクセルファイル（.xlsx）を選択してください", type=["xlsx"])

def process_data(file):
    try:
        # 1. エクセルの5行目（skiprows=4）にある合計数値を読み込む
        df_total_row = pd.read_excel(file, skiprows=4, nrows=1, dtype=str, header=None)
        
        # 2. 選手データ（見出しが6行目にある）を読み込む
        df_main = pd.read_excel(file, header=5, dtype=str)
        
        # 合計行の列名をメインデータと一致させる
        df_total_row.columns = df_main.columns
        df_total_row['選手'] = '【合計】'
        df_total_row['球団'] = 'ー'
        
        original_cols = df_main.columns.tolist()
        
        # --- 並べ替えロジック ---
        df_no_total = df_main[~df_main['選手'].str.contains('合計', na=False)].copy()
        
        # トヨタとそれ以外に分離
        df_toyota = df_no_total[df_no_total['球団'] == 'トヨタ'].copy()
        df_others = df_no_total[df_no_total['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
            if target_df.empty: return target_df
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号順（数字抽出）でソート
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        df_toyota_sorted = sort_group(df_toyota)
        df_others_sorted = sort_group(df_others)

        # 3. 合体（トヨタ -> その他 -> エクセルの合計）
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total_row], ignore_index=True)
        df_display = df_display[original_cols]

        return df_display
    except Exception as e:
        st.error(f"解析エラー: {e}\nエクセルの形式（5行目が合計、6行目が見出し）を確認してください。")
        return None

# --- メイン処理 ---
if uploaded_file is not None:
    df_result = process_data(uploaded_file)
    
    if df_result is not None:
        # 選手選択フィルター（左側のサイドバー）
        player_list = df_result[df_result['選手'] != '【合計】']['選手'].unique().tolist()
        selected = st.sidebar.multiselect("表示する選手を選択（未選択で全員表示）", player_list)
        
        display_final = df_result.copy()
        if selected:
            # 選択された選手 + 合計行を維持
            display_final = df_result[df_result['選手'].isin(selected) | (df_result['選手'] == '【合計】')]

        # 書式設定（見た目をエクセルに合わせる）
        format_dict = {}
        for col in display_final.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                # 三振率や合計の「6.70」などの文字をそのまま維持
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("アップロード完了！")
        st.dataframe(display_final.style.format(format_dict), use_container_width=True, hide_index=True)
else:
    st.info("上のボタンからエクセルファイルをアップロードしてください。")
