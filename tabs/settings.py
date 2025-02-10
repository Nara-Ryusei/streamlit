import streamlit as st
import openai
import os


def settings_tab():
    st.write("### 設定")

    # secrets.tomlから設定
    api_key = st.text_input(
        "OpenAI API Key", type="password", value=st.secrets.get("api_key", "")
    )
    model = st.secrets.get("model", "gpt-4o")

    try:
        openai.api_key = api_key
        models = openai.models.list()
        model_names = [model.id for model in models.data]
        default_index = model_names.index(model) if model in model_names else 0
        selected_model = st.selectbox("モデルを選択", model_names, index=default_index)
    except Exception as e:
        st.error(f"モデル一覧の取得に失敗しました: {e}")

    if st.button("保存"):
        if api_key:
            # session_stateに保存
            st.session_state["api_key"] = api_key
            st.session_state["model"] = selected_model
            # secrets.toml に保存
            os.makedirs(".streamlit", exist_ok=True)
            with open(".streamlit/secrets.toml", "w") as f:
                f.write(f"api_key = '{api_key}'\n")
                f.write(f"model = '{selected_model}'\n")
            st.success("設定を保存しました。")
