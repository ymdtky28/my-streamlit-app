import pandas as pd
import subprocess
import sys

# 表をきれいに表示するためのライブラリを自動インストール
try:
    from tabulate import tabulate
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    from tabulate import tabulate

def show_batting_stats(file_path):
    try:
        # ファイル読み込み
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # 列名の余計なスペースなどを削除
        df.columns = df.columns.str.strip()

        # 1. 選手ごとに合計値を算出
        summary = df.groupby('名前').sum(numeric_only=True).reset_index()

        # 2. 指標の計算（エラー回避用：打数が0なら0にする）
        summary['打率'] = (summary['安打'] / summary['打数']).fillna(0)
        
        obp_num = summary['安打'] + summary['四球'] + summary['死球']
        obp_den = summary['打数'] + summary['四球'] + summary['死球'] + summary['犠飛']
        summary['出塁率'] = (obp_num / obp_den).fillna(0)
        
        singles = summary['安打'] - (summary['二塁打'] + summary['三塁打'] + summary['本塁打'])
        total_bases = (singles * 1) + (summary['二塁打'] * 2) + (summary['三塁打'] * 3) + (summary['本塁打'] * 4)
        summary['長打率'] = (total_bases / summary['打数']).fillna(0)
        
        summary['OPS'] = (summary['出塁率'] + summary['長打率']).round(3)

        # 3. 見た目を整える
        for col in ['打率', '出塁率', '長打率']:
            summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

        # 4. 表示
        display_cols = ['名前', '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
        print("\n=== 最新の通算打撃成績 ===")
        print(tabulate(summary[display_cols], headers='keys', tablefmt='grid', showindex=False))
        
    except FileNotFoundError:
        print(f"【エラー】ファイル '{file_path}' が見つかりません。ファイル名が合っているか確認してください。")
    except KeyError as e:
        print(f"【エラー】エクセルの項目名が足りません。 {e} という列があるか確認してください。")
    except Exception as e:
        print(f"【エラー】予期せぬエラーが発生しました: {e}")

# --- 実行 ---
# ここにファイル名を入れてください
show_batting_stats('1.xlsx - Sheet1.csv')
