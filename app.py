import pandas as pd

def show_batting_stats(file_path):
    # エクセル（またはCSV）の読み込み
    try:
        # アップロードされたファイル形式に合わせて読み込み
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # 1. 選手ごとに合計値を算出（名前で名寄せ）
        summary = df.groupby('名前').sum(numeric_only=True).reset_index()

        # 2. 指標の計算
        # 打率 (AVG)
        summary['打率'] = (summary['安打'] / summary['打数']).fillna(0).apply(lambda x: f"{x:.3f}".replace('0.', '.'))
        
        # 出塁率 (OBP)
        obp_num = summary['安打'] + summary['四球'] + summary['死球']
        obp_den = summary['打数'] + summary['四球'] + summary['死球'] + summary['犠飛']
        summary['出塁率'] = (obp_num / obp_den).fillna(0).apply(lambda x: f"{x:.3f}".replace('0.', '.'))
        
        # 長打率 (SLG)
        singles = summary['安打'] - (summary['二塁打'] + summary['三塁打'] + summary['本塁打'])
        total_bases = (singles * 1) + (summary['二塁打'] * 2) + (summary['三塁打'] * 3) + (summary['本塁打'] * 4)
        summary['長打率'] = (total_bases / summary['打数']).fillna(0).apply(lambda x: f"{x:.3f}".replace('0.', '.'))
        
        # OPS (出塁率 + 長打率)
        # 数値計算用に一旦計算
        ops_val = (obp_num / obp_den).fillna(0) + (total_bases / summary['
