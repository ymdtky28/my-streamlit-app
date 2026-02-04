import pandas as pd

def load_baseball_stats(file_path):
    # ファイルの読み込み（3行目付近にヘッダーがあるため header=None で読み込み後に調整）
    df = pd.read_csv(file_path, header=None)
    
    # データの基本クレンジング
    # 列名が複雑なため、用途に合わせてスライスして利用するのが効率的です
    
    # 例: 打撃成績（全試合合計）の部分だけを抽出
    # 0~21列目が「合計(全試合)」の打撃データと想定
    batting_total = df.iloc[:, [0, 1, 2, 3, 4, 6, 18, 19]] # 選手名, 出場数, 打席, 打数, 安打, 打率など
    batting_total.columns = ['選手名', '出場数', '打席', '打数', '安打', '本塁打', '三振', '打率']
    
    # 数値変換（空文字やNaNを0に置き換え）
    batting_total = batting_total.dropna(subset=['選手名'])
    
    return batting_total

# 2025年と2026年のデータを読み込み
df_2025 = load_baseball_stats('成績表.xlsx - 2025.csv')
df_2026 = load_baseball_stats('成績表.xlsx - 2026.csv')

# 表示例
print("--- 2025年 打撃成績（抜粋） ---")
print(df_2025.head(10))
