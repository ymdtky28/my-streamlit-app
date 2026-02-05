import os
import subprocess
import sys

# 1. 不足しているライブラリを自動でインストールする関数
def install_libraries():
    libraries = ["pandas", "openpyxl", "tabulate"]
    for lib in libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"部品({lib})を準備しています。少々お待ちください...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libraries()

import pandas as pd
from tabulate import tabulate

def main():
    # --- 設定：読み込むファイル名をここに合わせてください ---
    # 先ほどアップロードされたファイル名が「1.xlsx - Sheet1.csv」だったのでそれを指定しています
    file_path = '1.xlsx - Sheet1.csv' 
    
    if not os.path.exists(file_path):
        print(f"【エラー】'{file_path}' というファイルが見つかりません。")
        print("ファイル名を 'data.xlsx' などに変更するか、コード内のファイル名を書き換えてください。")
        return

    try:
        # 2. データの読み込み
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # 列名の空白などを除去してエラーを防ぐ
        df.columns = df.columns.str.strip()

        # 3. 集計処理
        summary = df.groupby('名前').sum(numeric_only=True).reset_index()

        # 4. 指標の計算
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

        # 5. 野球らしい表記 (.333) に変換
        for col in ['打率', '出塁率', '長打率']:
            summary[col] = summary[col].apply(lambda x: f"{x:.3f}".replace('0.', '.'))

        # 6. 結果の表示
        cols = ['名前', '打数', '安打', '二塁打', '三塁打', '本塁打', '打点', '打率', '出塁率', 'OPS']
        print("\n" + "="*50)
        print("          ⚾️ 最新 通算成績表 ⚾️")
        print("="*50)
        print(tabulate(summary[cols], headers='keys', tablefmt='grid', showindex=False))
        
    except Exception as e:
        print(f"【エラーが発生しました】\n{e}")

if __name__ == "__main__":
    main()
