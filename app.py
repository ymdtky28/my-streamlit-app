import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績集計", layout="wide")
st.title("⚾️ 野球成績集計アプリ")

uploaded_file = st.file_uploader("成績ファイル（CSVまたはExcel）を選択してください", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # 1. まずはそのまま読み込む
        if uploaded_file.name.endswith('.csv'):
            try:
                df_raw = pd.read_csv(uploaded_file, encoding='utf-8', header=None)
            except:
                uploaded_file.seek(0)
                df_raw = pd.read_csv(uploaded_file, encoding='shift-jis', header=None)
        else:
            df_raw = pd.read_excel(uploaded_file, header=None)

        # 2. 「選手」という文字が入っているセルを探す
        start_row = 0
        found = False
        for i, row in df_raw.iterrows():
            if row.astype(str).str.contains('選手').any():
                start_row = i
                found = True
                break
        
        if found:
            # 「選手」が見つかった行を見出しとしてデータを再設定
            df = df_raw.iloc[start_row:].copy()
            df.columns = df.iloc[0] # 最初の行を見出しにする
            df = df.iloc[1:].reset_index(drop=True) # データ本体のみ抽出
            
            # 列名の空白を削除し、数値に変換できる列は変換する
            df.columns = df.columns.str.strip()
            # 「選手」列を「名前」として扱う
            name_col = '選手'
        else:
            st.error("ファイル内に「選手」という見出しが見つかりませんでした。")
            st.stop()

        # 数値列を強制的に数値型に変換（エラーは無視してNaNにする）
        cols_to_fix = ['打数', '安打数', '二塁打', '三塁打', '本塁打', '四死球', '犠飛', '打点']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 選手ごとに合計を集計
        summary = df.groupby(name_col).sum(numeric_only=True).reset_index()

        # --- 指標の計算 (0除算対策込み) ---
        ab = summary['打数']
        h = summary['安打数']
        h2 = summary['二塁打']
        h3 = summary['三塁打']
        hr = summary['本塁打']
        hbp_bb = summary['四死球']
        sf = summary['犠飛']

        # 打率
        summary['打率'] = (h / ab).where(ab > 0, 0)
        
        # 出塁率
        obp_den = ab + hbp_bb + sf
        summary['出塁率'] = ((h + hbp_bb) / obp_den).where(obp_den > 0, 0)
        
        # 長打率
        singles = h - (h2 + h3 + hr)
        total_bases = (singles * 1) + (h2 * 2) + (h3 * 3) + (hr * 4)
        summary['長打率'] = (total_bases / ab).where(ab > 0, 0)
        
        # OPS
        summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

        # 野球表記 (.333) に整える
        for col in ['打率', '出塁率', '長打率']:
            summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

        st.success("✅ 「選手」行を基準に集計が完了しました！")
        
        # 表示する列
        display_cols = [name_col, '打数', '安打数', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
        available_cols = [c for c in display_cols if c in summary.columns]
        
        st.dataframe(summary[available_cols], use_container_width=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
