import pandas as pd
import os

def update_stats(new_file_path, master_file='total_stats.xlsx'):
    # 1. 新しい試合データの読み込み
    df_new = pd.read_excel(new_file_path)
    
    # 2. 過去の全データ（master_file）があれば読み込み、なければ新規作成
    if os.path.exists(master_file):
        df_master_all_games = pd.read_excel('raw_data_history.xlsx') # 全試合の生データ
        df_combined = pd.concat([df_master_all_games, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # 全試合の生データを保存（バックアップ用）
    df_combined.to_excel('raw_data_history.xlsx', index=False)

    # 3. 選手名で集計
    summary = df_combined.groupby('名前').sum(numeric_only=True).reset_index()

    # 4. 指標の計算
    # 打率 (AVG) = 安打 / 打数
    summary['打率'] = (summary['安打'] / summary['打数']).fillna(0).round(3)
    
    # 出塁率 (OBP)
    obp_num = summary['安打'] + summary['四球'] + summary['死球']
    obp_den = summary['打数'] + summary['四球'] + summary['死球'] + summary['犠飛']
    summary['出塁率'] = (obp_num / obp_den).fillna(0).round(3)
    
    # 長打率 (SLG)
    singles = summary['安打'] - (summary['二塁打'] + summary['三塁打'] + summary['本塁打'])
    total_bases = (singles * 1) + (summary['二塁打'] * 2) + (summary['三塁打'] * 3) + (summary['本塁打'] * 4)
    summary['長打率'] = (total_bases / summary['打数']).fillna(0).round(3)
    
    # OPS = 出塁率 + 長打率
    summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

    # 5. 最新の通算成績を保存
    summary.to_excel(master_file, index=False)
    print(f"成功！'{master_file}' に最新の成績を書き出しました。")

# --- 使い方 ---
# update_stats('今日の試合結果.xlsx')
