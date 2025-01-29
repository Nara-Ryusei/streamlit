import os
import streamlit as st
from openai import OpenAI, APIConnectionError

# OpenAI APIキーを設定
if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])
else:
    st.error("API Keyが設定されていません。設定タブでAPI Keyを入力してください。")

# セッションステートを初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

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
selected_file = st.selectbox("対象のアプリを選択してください:", file_list)

# メッセージ履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け取る
if prompt := st.chat_input("何をお手伝いしますか？"):
    # ユーザーのメッセージを履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    # チャットメッセージとして表示
    with st.chat_message("user"):
        st.markdown(prompt)

    file_path = os.path.join(pages_path, selected_file) + ".py"
    # ファイル内容読み取り
    with open(file_path, "r") as file:
        file_content = file.read()

    try:
        # OpenAI APIを使ってAIからの応答をストリーミングで生成
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"以下の内容について回答してください\n\n{file_content}",
                },
                *st.session_state.messages,
            ],
            stream=True,  # ストリーミングを有効にする
        )

        # AIのメッセージをチャンクごとに表示
        with st.chat_message("assistant"):
            full_response = ""
            placeholder = st.empty()  # プレースホルダーを作成
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None:
                    full_response += content
                    placeholder.markdown(full_response + "▌")  # 途中経過を表示
            placeholder.markdown(full_response)  # 最終的な応答を表示

        # AIのメッセージを履歴に追加
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except APIConnectionError:
        st.error("サーバー接続エラー。 home > 設定タブからOpenAI API Keyを確認してください。")
