import streamlit as st
import os

# ページの幅をワイドに設定
st.set_page_config(layout="wide")
# タイトルと内容を入力
st.title("Streamlit × OpenAI")

# セッションステートにAPIキーがなければ初期化
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# secrets.toml ファイルが存在するか確認
secrets_path = ".streamlit/secrets.toml"
if not os.path.exists(secrets_path):
    os.makedirs(".streamlit", exist_ok=True)
    with open(secrets_path, "w") as f:
        f.write("")

# APIキーが設定されていない場合の警告メッセージ
show_warning = not st.secrets.get("api_key")

# タブを作成
tab1, tab2, tab3, tab4 = st.tabs(["新規作成", "更新", "削除", "設定"])

with tab1:
    from tabs.create import create_tab

    create_tab()

with tab2:
    from tabs.update import update_tab

    update_tab()

with tab3:
    from tabs.delete import delete_tab

    delete_tab()

with tab4:
    from tabs.settings import settings_tab

    settings_tab()

    # 設定タブでAPIキーが設定されたら警告メッセージを消す
    if st.session_state["api_key"]:
        show_warning = False

if show_warning:
    st.warning("設定タブからOpenAI API Keyを設定してください")
