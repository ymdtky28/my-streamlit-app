import os
import streamlit as st

# 1. そもそも data フォルダがあるか？
if os.path.exists('data'):
    files = os.listdir('data')
    st.write("dataフォルダの中にあるファイルはこれです：")
    st.code(files) # ここに表示された名前をそのままコピーして使う
else:
    st.error("data フォルダ自体がリポジトリに存在しません！")

# 2. 今の場所（カレントディレクトリ）にある全てのファイル
st.write("すべてのファイル構成:")
for root, dirs, files in os.walk("."):
    for file in files:
        st.write(os.path.join(root, file))
