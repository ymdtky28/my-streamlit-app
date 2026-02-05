import streamlit as st
import pandas as pd
import io

# タイトルの設定
st.title("⚾️ 野球成績集計アプリ")

# --- 1. アップロード画面を表示 (Streamlit版) ---
uploaded_file = st.file_uploader("成績を管理するエクセル（またはCSV）を選択してください", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # --- 2. データの読み込み ---
    filename = uploaded_file.name
    if filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 項目名の空白を削除（エラー防止）
    df.columns = df.columns.str.strip()

    # 選手ごとに合計を集計
    summary = df.groupby('名前').sum(numeric_only=True).reset_index()

    # 指標の計算（打率・OPSなど）
    # 分母が0になる場合の対策として、単純な割り算ではなく fillna(0) を活用
    summary['打率'] = (summary['安打'] / summary['打数']).fillna(0)
    
    obp_num = summary['安打'] + summary.get('四球', 0) + summary.get('死球', 0)
    obp_den = summary['打数'] + summary.get('四球', 0) + summary.get('死球', 0) + summary.get('犠飛', 0)
    summary['出塁率'] = (obp_num / obp_den).fillna(0)
    
    # 長打率の計算
    singles = summary['安打'] - (summary.get('二塁打', 0) + summary.get('三塁打', 0) + summary.get('本塁打', 0))
    total_bases = (singles * 1) + (summary.get('二塁打', 0) * 2) + (summary.get('三塁打', 0) * 3) + (summary.get('本塁打', 0) * 4)
    summary['長打率'] = (total_bases / summary['打数']).fillna(0)
    summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

    # 野球表記 (.333) に整える
    for col in ['打率', '出塁率', '長打率']:
        summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

    # --- 3. 画面に表示 (Streamlit版) ---
    st.success(f"✅ {filename} の集計が完了しました！")
    
    # 表示する列の選択（データに列が存在する場合のみ）
    display_cols = ['名前', '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
    available_cols = [c for c in display_cols if c in summary.columns]
    
    st.dataframe(summary[available_cols])
