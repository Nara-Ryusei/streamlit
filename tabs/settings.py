import streamlit as st
import openai
import os

def settings_tab():
    st.write("### 設定")
    api_key = st.text_input(
        "OpenAI API Key", type="password", value=st.secrets.get("api_key", "")
    )
    if st.button("保存"):
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("API Keyが設定されました。")
            # secrets.toml に保存
            os.makedirs(".streamlit", exist_ok=True)
            with open(".streamlit/secrets.toml", "w") as f:
                f.write(f"api_key = '{api_key}'")
                openai.api_key = st.session_state["api_key"]
