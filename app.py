import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績アップローダー", layout="wide")
st.title("⚾ 野球成績 エクセルアップロード表示")

# --- ファイルアップローダー ---
uploaded_file = st.file_uploader("エクセルファイルをアップロードしてください", type=["xlsx"])

def process_data(file):
    try:
        # 1. エクセル最上部の合計行（5行目）を読み込む
        # skiprows=4 (5行目), nrows=1 (1行だけ)
        df_total_row = pd.read_excel(file, skiprows=4, nrows=1, dtype=str, header=None)
        
        # 2. 選手データ（見出しが6行目にある）を読み込む
        df_main = pd.read_excel(file, header=5, dtype=str)
        
        # 列名を合計行に適用
        df_total_row.columns = df_main.columns
        df_total_row['選手'] = '【合計】'
        df_total_row['球団'] = 'ー'
        
        original_cols = df_main.columns.tolist()
        
        # --- 並び替えロジック ---
        # 選手データを整理
        df_no_total = df_main[~df_main['選手'].str.contains('合計', na=False)].copy()
        
        # トヨタとそれ以外
        df_toyota = df_no_total[df_no_total['球団'] == 'トヨタ'].copy()
        df_others = df_no_total[df_no_total['球団'] != 'トヨタ'].copy()

        def sort_group(target_df):
            if target_df.empty: return target_df
            rika = target_df[target_df['選手'].str.contains('理化', na=False)].copy()
            others = target_df[~target_df['選手'].str.contains('理化', na=False)].copy()
            # 背番号順ソート
            others['sort_key'] = others['選手'].str.extract('(\d+)').astype(float)
            others = others.sort_values('sort_key').drop(columns=['sort_key'])
            return pd.concat([others, rika], ignore_index=True)

        df_toyota_sorted = sort_group(df_toyota)
        df_others_sorted = sort_group(df_others)

        # 最終結合（トヨタ -> その他 -> エクセルの合計）
        df_display = pd.concat([df_toyota_sorted, df_others_sorted, df_total_row], ignore_index=True)
        df_display = df_display[original_cols]

        return df_display
    except Exception as e:
        st.error(f"解析エラー: {e}")
        return None

if uploaded_file is not None:
    # アップロードされたファイルを処理
    df_result = process_data(uploaded_file)
    
    if df_result is not None:
        # --- 書式設定 ---
        format_dict = {}
        for col in df_result.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' and x != 'nan' else str(x)
            else:
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""

        st.success("アップロード完了！エクセルの見た目通りに表示しました。")
        st.dataframe(df_result.style.format(format_dict), use_container_width=True, hide_index=True)
else:
    st.info("上のボタンからエクセルファイル（.xlsx）を選択してください。")
