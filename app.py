import pandas as pd

def load_and_process_data(file_path):
    # CSVの読み込み（ヘッダーが5行目にあると想定）
    # 元データの構造に合わせて skiprows を調整してください
    df = pd.read_csv(file_path, skiprows=5)
    
    # 列名のクリーニング（余計な空白を削除）
    df.columns = [c.strip() for c in df.columns]
    
    # 数値列が文字列として読み込まれた場合の変換
    numeric_cols = ['打席', '打数', '安打', '二塁打', '三塁打', '本塁打', '四球', '死球', '犠飛']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

def calculate_stats(df):
    """
    抽出されたデータから打率、出塁率、長打率を再計算する
    """
    stats = df.copy()
    
    # 打率 = 安打 / 打数
    stats['打率'] = (stats['安打'] / stats['打数']).round(3)
    
    # 出塁率 = (安打 + 四球 + 死球) / (打数 + 四球 + 死球 + 犠飛)
    denominator_obp = stats['打数'] + stats['四球'] + stats['死球'] + stats['犠飛']
    stats['出塁率'] = ((stats['安打'] + stats['四球'] + stats['死球']) / denominator_obp).round(3)
    
    # 長打率 = 塁打数 / 打数
    # ※単打 = 安打 - (二塁打 + 三塁打 + 本塁打)
    # 塁打数 = 単打 + 2*二塁打 + 3*三塁打 + 4*本塁打
    if '塁打数' in stats.columns:
        stats['長打率'] = (stats['塁打数'] / stats['打数']).round(3)
        
    return stats

# --- メイン処理 ---
file_path = '打撃成績表_トヨタ全打者vs全投手.xlsx - Sheet1.csv'
raw_data = load_and_process_data(file_path)

# 1. 選手ごとに集計したい場合
player_summary = raw_data.groupby('選手').sum(numeric_only=True)
final_stats = calculate_stats(player_summary)

# 結果の表示（上位5名）
print(final_stats[['打席', '打数', '安打', '本塁打', '打率', '出塁率']].sort_values('打率', ascending=False).head())
