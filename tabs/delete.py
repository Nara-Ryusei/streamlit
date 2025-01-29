import streamlit as st
import os


def delete_tab():
    st.write("### 削除")

    # 編集禁止ファイルのリスト
    restricted_files = ["ChatGPT.py", "CodeEditor.py"]

    # アプリのタイトルを選択してくださいのセレクトボックス
    def get_pages_files():
        return [
            f.replace(".py", "")
            for f in os.listdir("pages")
            if f.endswith(".py") and f not in restricted_files
        ]

    pages_files = get_pages_files()
    delete_file = st.selectbox("削除するアプリを選択してください", pages_files)

    if st.button("削除"):
        if delete_file:
            try:
                file_path = os.path.join("pages", f"{delete_file}.py")
                os.remove(file_path)
                st.success(f"{delete_file} が削除されました。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
