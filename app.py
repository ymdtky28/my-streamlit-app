import pandas as pd
import io
from google.colab import files
from IPython.display import display

# --- 1. アップロード画面を表示 ---
print("⚾️ 成績を管理するエクセル（またはCSV）を選択してください...")
uploaded = files.upload()

# --- 2. データの読み込みと計算 ---
for filename in uploaded.keys():
    # データの読み込み
    df = pd.read_csv(io.BytesIO(uploaded[filename])) if filename.endswith('.csv') else pd.read_excel(io.BytesIO(uploaded[filename]))
    
    # 項目名の空白を削除（エラー防止）
    df.columns = df.columns.str.strip()

    # 選手ごとに合計を集計
    summary = df.groupby('名前').sum(numeric_only=True).reset_index()

    # 指標の計算（打率・OPSなど）
    summary['打率'] = (summary['安打'] / summary['打数']).fillna(0)
    obp_num = summary['安打'] + summary['四球'] + summary['死球']
    obp_den = summary['打数'] + summary['四球'] + summary['死球'] + summary['犠飛']
    summary['出塁率'] = (obp_num / obp_den).fillna(0)
    
    # 長打率の計算
    singles = summary['安打'] - (summary['二塁打'] + summary['三塁打'] + summary['本塁打'])
    total_bases = (singles * 1) + (summary['二塁打'] * 2) + (summary['三塁打'] * 3) + (summary['本塁打'] * 4)
    summary['長打率'] = (total_bases / summary['打数']).fillna(0)
    summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

    # 野球表記 (.333) に整える
    for col in ['打率', '出塁率', '長打率']:
        summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

    # --- 3. 画面に表示 ---
    cols = ['名前', '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
    print(f"\n✅ {filename} の集計が完了しました！")
    display(summary[cols])
