import streamlit as st
import openai
import os

def update_tab():
    st.write("### 更新")
    
    # 編集禁止ファイルのリスト
    restricted_files = ["ChatGPT.py", "CodeEditor.py"]

    # アプリのタイトルを選択してくださいのセレクトボックス
    def get_pages_files():
        return [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py") and f not in restricted_files]

    pages_files = get_pages_files()
    app_title = st.selectbox("更新するアプリを選択してください", pages_files)

    # 変更内容を入力するテキストボックス
    update_content = st.text_area("変更内容を入力してください")

    if st.button("更新"):
        if app_title and update_content.strip():
            try:
                # 選択されているファイルの内容を読み込む
                file_path = os.path.join("pages", f"{app_title}.py")
                with open(file_path, "r") as file:
                    existing_content = file.read()

                # OpenAI APIにリクエストを送信
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは有能なPythonエンジニアです。指定された内容を実現するPythonのソースコードのみを生成してください。説明や付随するコメントを一切含めないでください。実行可能なStreamlitコードだけを出力してください。```pythonも不要です。",
                        },
                        {
                            "role": "user",
                            "content": f"{existing_content}\n\n{update_content}",
                        },
                    ],
                )

                full_response = response.choices[0].message.content

                # 提案されたソースコードを保存
                with open(file_path, "w") as file:
                    file.write(full_response)
                st.success(f"{app_title} が更新されました。")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("アプリのタイトルと変更内容を入力してください。")
