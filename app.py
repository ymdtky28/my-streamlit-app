import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="野球成績集計", layout="wide")
st.title("⚾️ 野球成績集計アプリ")

uploaded_file = st.file_uploader("成績ファイル（CSVまたはExcel）を選択してください", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # データの読み込み
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='shift-jis')
        else:
            df = pd.read_excel(uploaded_file)

        # 列名の空白を削除
        df.columns = df.columns.str.strip()

        # 選手ごとに合計を集計
        # CSVの項目名「名前」でグループ化
        summary = df.groupby('名前').sum(numeric_only=True).reset_index()

        # --- 指標の計算 (CSVの項目名に合わせました) ---
        
        # 打数・安打などの取得（万が一列がない場合は0として扱う）
        ab = summary.get('打数', 0)
        h = summary.get('安打数', 0)
        h2 = summary.get('二塁打', 0)
        h3 = summary.get('三塁打', 0)
        hr = summary.get('本塁打', 0)
        hbp_bb = summary.get('四死球', 0)
        sf = summary.get('犠飛', 0)

        # 1. 打率 (安打数 / 打数)
        summary['打率'] = (h / ab).fillna(0)
        
        # 2. 出塁率 ( (安打数 + 四死球) / (打数 + 四死球 + 犠飛) )
        obp_den = ab + hbp_bb + sf
        summary['出塁率'] = ((h + hbp_bb) / obp_den).fillna(0)
        
        # 3. 長打率
        # 単打 = 安打数 - (二塁打 + 三塁打 + 本塁打)
        singles = h - (h2 + h3 + hr)
        total_bases = (singles * 1) + (h2 * 2) + (h3 * 3) + (hr * 4)
        summary['長打率'] = (total_bases / ab).fillna(0)
        
        # 4. OPS (出塁率 + 長打率)
        summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

        # 野球表記 (.333) に整える
        for col in ['打率', '出塁率', '長打率']:
            summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

        st.success("✅ 集計が完了しました！")
        
        # 表示する列の並び替え
        cols = ['名前', '打数', '安打数', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
        available_cols = [c for c in cols if c in summary.columns]
        
        st.dataframe(summary[available_cols], use_container_width=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
