import streamlit as st
import pandas as pd

# 1. エラーの原因だった関数を正しく定義
def sort_group(target_df, column_name):
    # 列名が存在するかチェックして並び替える
    if column_name in target_df.columns:
        return target_df.sort_values(by=column_name, ascending=False)
    return target_df

st.title("打撃成績分析アプリ")

# 2. CSVファイルの読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    # データ読み込み（Shift-JISなどでエラーが出る場合は encoding='cp932' を追加）
    df = pd.read_csv(uploaded_file)
    
    # 3. 並び替え対象の列を選択するUI
    # CSVにある「打率」や「安打」などを選択できるようにします
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    sort_key = st.selectbox("並び替えの基準を選んでください", numeric_cols)
    
    # 4. 関数を呼び出して結果を表示
    st.subheader(f"{sort_key} 順のデータ")
    sorted_df = sort_group(df, sort_key)
    st.dataframe(sorted_df)
else:
    st.info("CSVファイルをアップロードするとデータが表示されます。")
