import streamlit as st
import openai
import os

def create_tab():
    st.write("### 新規作成")

    # タイトルと内容を追加
    input_title = st.text_input("タイトルを入力してください")
    input_content = st.text_area("内容を入力してください")

    # 依頼ボタンを追加
    if st.button("生成"):
        if input_content.strip():
            try:
                # OpenAI APIにリクエストを送信
                stream = openai.chat.completions.create(  # 注意: 最新のAPIエンドポイント使用
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは有能なPythonエンジニアです。説明を一切含めないでください。実行可能なStreamlitコードだけを出力し、コードの説明は一切含めないでください。```pythonも不要です。1ファイルで完結するようにしてください。",
                        },
                        {"role": "user", "content": input_content},
                    ],
                    stream=True,  # ストリーミングを有効化
                )

                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content

                # 提案されたソースコードを保存
                if input_title:
                    file_path = os.path.join("pages", f"{input_title}.py")
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(full_response)
                    st.success(f"{input_title}が生成されました。")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("入力欄が空です。質問を入力してください。")
