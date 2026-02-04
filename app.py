# --- 集計と書式設定 ---
    try:
        numeric_cols = df.select_dtypes(include=['number']).columns
        # 1. まずは単純に各項目の合計を出す
        df_sum = df.groupby(['選手', '球団'])[numeric_cols].sum().reset_index()
        
        # 2. 三振率を「打席 ÷ 三振」で正しく再計算
        # 三振が0だとエラーになるため、0の場合は0を表示するようにします
        def calculate_so_rate(row):
            if '三振' in row and row['三振'] > 0:
                return row['打席'] / row['三振']
            return 0

        df_sum['三振率'] = df_sum.apply(calculate_so_rate, axis=1)
        
        # 3. 全体合計行の作成と、合計行の三振率再計算
        total_values = df_sum[numeric_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        total_df['三振率'] = calculate_so_rate(total_df.iloc[0])
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 4. 書式設定
        format_dict = {}
        for col in numeric_cols:
            if col == '三振率':
                # 三振率は小数点第2位までの「普通の数字」で表示（例: 15.25）
                format_dict[col] = "{:.2f}" 
            else:
                # 安打数などは整数
                format_dict[col] = "{:.0f}"
            
        # 打率などの「率」だけを野球形式（.300）にする
        rate_cols = ['打率', '長打率', '出塁率', '得点圏']
        for col in rate_cols:
            if col in df_display.columns:
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""

        st.success("三振率（打席/三振）を再計算して表示しました")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
