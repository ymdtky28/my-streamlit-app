import pandas as pd
import io
from google.colab import files

# 1. ファイルのアップロード
print("成績管理エクセル（またはCSV）を選択してください。")
uploaded = files.upload()

# 2. データの読み込み
for filename in uploaded.keys():
    # 拡張子によって読み込み方を変える
    if filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(uploaded[filename]))
    else:
        df = pd.read_excel(io.BytesIO(uploaded[filename]))

    # 列名の空白（スペース）を除去
    df.columns = df.columns.str.strip()

    # 3. 成績の集計（同じ名前の選手を合算）
    summary = df.groupby('名前').sum(numeric_only=True).reset_index()

    # 4. 指標の計算（打率・OPSなど）
    # 打率
    summary['打率'] = (summary['安打'] / summary['打数']).fillna(0)
    # 出塁率
    obp_num = summary['安打'] + summary['四球'] + summary['死球']
    obp_den = summary['打数'] + summary['四球'] + summary['死球'] + summary['犠飛']
    summary['出塁率'] = (obp_num / obp_den).fillna(0)
    # 長打率
    singles = summary['安打'] - (summary['二塁打'] + summary['三塁打'] + summary['本塁打'])
    total_bases = (singles * 1) + (summary['二塁打'] * 2) + (summary['三塁打'] * 3) + (summary['本塁打'] * 4)
    summary['長打率'] = (total_bases / summary['打数']).fillna(0)
    # OPS
    summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

    # 5. 野球流の表記 (.333) に整える
    for col in ['打率', '出塁率', '長打率']:
        summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

    # 6. 結果の表示
    cols = ['名前', '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
    print("\n--- 最新の集計成績 ---")
    # notebook形式できれいに表示
    from IPython.display import display
    display(summary[cols])
