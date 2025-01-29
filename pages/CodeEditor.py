from streamlit_monaco import st_monaco
import streamlit as st
import os

# デフォルトファイルのリスト
default_files = ["ChatGPT.py", "CodeEditor.py"]

def get_pages_files():
    return [
        f.replace(".py", "")
        for f in os.listdir("pages")
        if f.endswith(".py") and f not in default_files
    ]

pages_path = "./pages"
file_list = get_pages_files()

# ファイルを選択するドロップダウンメニュー
selected_file = st.selectbox("編集するファイルを選択してください:", file_list)

if selected_file:
    file_path = f"{pages_path}/{selected_file}.py"
    with open(file_path, "r") as file:
        content = file.read()

    content = st_monaco(value=content, height="600px", language="python", theme="vs-dark")

    if st.button("保存"):
        with open(file_path, "w") as file:
            file.write(content)
        st.success(f"{selected_file} が保存されました。")