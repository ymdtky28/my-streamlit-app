# データを読み込む
df_2025 = load_baseball_stats('data/成績表.xlsx - 2025.csv')

# 【重要】これを書かないと画面には何も出ません
if df_2025 is not None:
    st.write("### 2025年 成績表")
    st.dataframe(df_2025)
