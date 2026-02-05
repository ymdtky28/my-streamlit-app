import pandas as pd
import os

def update_baseball_stats(new_game_file, master_file='master_stats.xlsx'):
    # 1. 新しい試合データの読み込み
    df_new = pd.read_excel(new_game_file)
    
    # 2. 蓄積データの読み込み（存在しない場合は新規作成）
    if os.path.exists(master_file):
        df_master = pd.read_excel(master_file)
        # 過去の生データと今回のデータを結合
        df_combined = pd.concat([df_master, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # 3. 選手ごとに集計（合計値を算出）
    # ※「名前」を軸に、各数値を合計します
    stats_summary = df_combined.groupby('名前').sum(numeric_only=True).reset_index()

    # 4. 指標の自動計算（打率、出塁率、長打率、OPS）
    # 打率 (AVG)
    stats_summary['打率'] = (stats_summary['安打'] / stats_summary['打数']).fillna(0).round(3)
    
    # 出塁率 (OBP)
    numerator_obp = stats_summary['安打'] + stats_summary['四球'] + stats_summary['死球']
    denominator_obp = stats_summary['打数'] + stats_summary['四球'] + stats_summary['死球'] + stats_summary['犠飛']
    stats_summary['出塁率'] = (numerator_obp / denominator_obp).fillna(0).round(3)
    
    # 長打率 (SLG)
    single = stats_summary['安打'] - (stats_summary['二塁打'] + stats_summary['三塁打'] + stats_summary['本塁打'])
    total_bases = (single * 1) + (stats_summary['二塁打'] * 2) + (stats_summary['三塁打'] * 3) + (stats_summary['本塁打'] * 4)
    stats_summary['長打率'] = (total_bases / stats_summary['打数']).fillna(0).round(3)
    
    # OPS
    stats_summary['OPS'] = (stats_summary['出塁率'] + stats_summary['長打率']).round(3)

    # 5. 結果を保存
    stats_summary.to_excel(master_file, index=False)
    print(f"集計完了！ '{master_file}' を更新しました。")
    return stats_summary

# 使い方：ここにアップロードしたファイル名を入れます
# update_baseball_stats('game_20240520.xlsx')
