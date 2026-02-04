# --- 集計と書式設定 ---
    try:
        # 1. 計算する列（安打など）と、そのまま出す列（三振率）を分ける
        all_cols = df.columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 三振率を計算(sum)から完全に除外する
        calc_cols = [c for c in numeric_cols if c != '三振率']
        
        # 2. 三振率以外の合計を計算
        df_sum = df.groupby(['選手', '球団'])[calc_cols].sum().reset_index()
        
        # 3. 三振率は計算せず、元のデータの「文字」をそのまま持ってくる
        if '三振率' in df.columns:
            # 蓄積データの場合、その選手の「最新行」の三振率を表示させる
            so_rate_df = df.groupby(['選手', '球団'])['三振率'].last().reset_index()
            df_sum = pd.merge(df_sum, so_rate_df, on=['選手', '球団'], how='left')

        # 4. 全体合計行の作成
        total_values = df_sum[calc_cols].sum()
        total_df = pd.DataFrame(total_values).T
        total_df['選手'] = '【合計】'
        total_df['球団'] = 'ー'
        if '三振率' in df_sum.columns:
            total_df['三振率'] = 'ー' # 全体合計の三振率は意味がないのでハイフン
        
        df_display = pd.concat([df_sum, total_df], ignore_index=True)

        # 5. 【重要】表示フォーマットの出し分け
        format_dict = {}
        for col in df_display.columns:
            if col in ['打率', '長打率', '出塁率', '得点圏']:
                # 野球形式 (.300) に変換
                format_dict[col] = lambda x: f"{float(x):.3f}".replace("0.", ".") if pd.notnull(x) and x != '' else ""
            elif col == '三振率':
                # Excelの見た目（8.00 や 11.20）をそのまま文字列として出す
                format_dict[col] = lambda x: str(x) if pd.notnull(x) else ""
            elif col in calc_cols:
                # 安打、打点などは小数点を消して整数にする
                format_dict[col] = "{:.0f}"
        
        st.success("三振率はExcelの入力値をそのまま表示しています")
        st.dataframe(df_display.style.format(format_dict), use_container_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.dataframe(df)
