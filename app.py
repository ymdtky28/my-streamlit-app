import streamlit as st
import pandas as pd
import os

st.title("デバッグモード：ファイル確認")

# 1. 現在の場所にあるファイルを表示
st.write("### 現在のディレクトリのファイル一覧")
st.code(os.listdir('.'))

# 2. dataフォルダの中身を表示
if os.path.exists('data'):
    st.write("### dataフォルダ内のファイル一覧")
    st.code(os.listdir('data'))
else:
    st.error("エラー：'data' という名前のフォルダが見つかりません。")

# 3. 読み込みテスト
def load_data():
   # data を date に一文字変えるだけです！
target = 'date/成績表.xlsx - 2025.csv'
