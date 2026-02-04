# --- 集計と書式設定 ---
    try:
        # 1. 数字列のリストを取得
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        # 2. 三振率以外の合計を計算
        # ※三振率を合計(sum)に含めると数字が跳ね上がるため、集計対象から一旦外すか、後で調整します
        other_cols = [c for c in numeric_cols if c != '三振率']
        df_sum = df.groupby(['選手', '球団'])[other_cols].sum().reset_index()
        
        # 3. 三振率は「蓄積」ではなく「最新の1行」または「元のまま」を表示する場合
        # 蓄積データで同じ選手が複数行ある場合、ここでは「平均」または「最初の値」を取得します
        if '三振率' in df.columns:
            so_rate = df.groupby(['選手', '球団'])['三振率'].first().reset_index()
            df_sum = pd.merge(df_sum, so_rate, on=['選手', '球団'])

        # 4. 全体合計行の作成
        total_values = df_sum[other_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        # 合計行の三振率は空欄（またはハイフン）にする
        if '三振率' in df.columns:
            total_df['三振率'] = None
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 5. 書式設定
        format_dict = {}
        for col in numeric_cols:
            if col == '三振率':
                # 三振率は何も加工しない（Excelの見た目そのまま）
                format_dict[col] = lambda x: x if pd.notnull(x) else ""
            else:
                # 安打数などは整数
                format_dict[col] = "{:.0f}"
            
        # 打率などの「率」だけを野球形式（.300）にする
        rate_cols = ['打率', '長打率', '出塁率', '得点圏']
        for col in rate_cols:
            if col in df_display.columns:
                format_dict[col] = lambda x: f"{x:.3f}".replace("0.", ".") if pd.notnull(x) else ""

        st.success("表示を更新しました（三振率は入力値をそのまま表示）")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
