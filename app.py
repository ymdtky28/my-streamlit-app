import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="野球成績蓄積", layout="wide")
st.title("⚾ 野球成績 期間・試合別表示")

target = 'data.csv.xlsx'

def load_data():
    if os.path.exists(target):
        try:
            # 1. 三振率を文字列として読み込み保護
            df_raw = pd.read_excel(target, header=5, dtype=str)
            df = df_raw.copy()
            
            # 列の順番を記憶
            column_order = df.columns.tolist()
            
            # 計算用列を数値変換
            numeric_cols = [c for c in df.columns if c not in ['選手', '球団', '日付', '試合名', '三振率']]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            if '日付' in df.columns:
                df['日付'] = pd.to_datetime(df['日付'])
                
            return df, column_order
        except Exception as e:
            st.error(f"読み込みエラー: {e}")
            return None, None
    return None, None

df, original_cols = load_data()

if df is not None:
    try:
        calc_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 2. 集計処理
        agg_dict = {col: 'sum' for col in calc_cols}
        if '三振率' in df.columns:
            agg_dict['三振率'] = 'last'
            
        df_sum = df.groupby(['選手', '球団']).agg(agg_dict).reset_index()

        # --- 3. 並び替え処理 (#0, #1... の順にする) ---
        # 選手名の先頭にある数字を抜き出して並び替える
        df_sum['sort_key'] = df_sum['選手'].str.extract('(\d+)').astype(float)
        df_sum = df_sum.sort_values('sort_key').drop(columns=['sort_key'])

        # 4. 元の列順に戻す
        current_cols = df_sum.columns.tolist()
        df_sum = df_sum[[c for c in original_cols if c in current_cols]]

        # 5. 合計行の作成（一番下に結合）
        total_values = df_sum[calc_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー'
        
        # 選手データ + 合計行 の順で合体
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 6. 表示フォーマット
        format_dict = {}
        for col in df_display.columns:
            if col == '三振率':
                format_dict[col] = lambda x: str(x) if pd.notnull(x) and str(x) != 'nan' else ""
            elif col in ['打率', '長打率', '出塁率', '得点圏']:
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and str(x) != 'nan' else ""
            elif col in calc_cols:
                format_dict[col] = "{:.0f}"

        # インデックスを表示しない設定で表を出す
        st.dataframe(df_display.style.format(format_dict), use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"エラー: {e}")
        st.dataframe(df)
        
