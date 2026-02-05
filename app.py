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
            # Shift_JIS(日本語Windows)とUTF-8の両方に対応
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='shift-jis')
        else:
            df = pd.read_excel(uploaded_file)

        # 列名の空白を削除
        df.columns = df.columns.str.strip()

        st.info("💡 読み込んだデータの最初の5行:")
        st.write(df.head())

        # --- 列の選択 ---
        st.divider()
        st.subheader("⚙️ 設定")
        
        all_columns = df.columns.tolist()
        
        # 「名前」に近い列名を自動で推測
        default_name_col = next((c for c in all_columns if "名前" in c or "氏名" in c or "選手" in c), all_columns[0])
        
        name_column = st.selectbox("「名前」が書かれている列を選んでください", all_columns, index=all_columns.index(default_name_col))

        if st.button("集計を実行する"):
            # 集計処理
            summary = df.groupby(name_column).sum(numeric_only=True).reset_index()

            # 指標の計算（列が存在しない場合に備えて .get() を使用）
            def get_val(col_name):
                return summary[col_name] if col_name in summary.columns else 0

            at_bats = get_val('打数')
            hits = get_val('安打')
            h2 = get_val('二塁打')
            h3 = get_val('三塁打')
            hr = get_val('本塁打')
            bb = get_val('四球')
            hbp = get_val('死球')
            sf = get_val('犠飛')

            # 打率
            summary['打率'] = (hits / at_bats).fillna(0)
            
            # 出塁率
            obp_num = hits + bb + hbp
            obp_den = at_bats + bb + hbp + sf
            summary['出塁率'] = (obp_num / obp_den).fillna(0)
            
            # 長打率
            singles = hits - (h2 + h3 + hr)
            total_bases = (singles * 1) + (h2 * 2) + (h3 * 3) + (hr * 4)
            summary['長打率'] = (total_bases / at_bats).fillna(0)
            
            # OPS
            summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

            # 野球表記に変換
            for col in ['打率', '出塁率', '長打率']:
                summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

            st.success("✅ 集計が完了しました！")
            
            # 表示する列（存在する列だけ表示）
            display_candidates = [name_column, '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
            available_display = [c for c in display_candidates if c in summary.columns]
            
            st.dataframe(summary[available_display], use_container_width=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
