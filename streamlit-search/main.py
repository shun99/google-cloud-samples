import os
import streamlit as st
import vertexai
from logger import Logger
from chat import Chat
from gemini import Gemini
from search import Search
from google.protobuf.json_format import MessageToDict

e = os.environ
PROJECT_ID = e.get("GOOGLE_CLOUD_PROJECT")
DATA_STORE_ID = e.get("DATA_STORE_ID")
MODEL_LOCATION = e.get("MODEL_LOCATION", "asia-northeast1")
LOCATION = e.get("LOCATION", "global")

# アプリよりユーザーIDを取得
user="ユーザー1"

# Logger初期化
logger = Logger()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat初期化
chat = Chat(PROJECT_ID, MODEL_LOCATION)

# Gemini初期化
gemini = Gemini(PROJECT_ID, MODEL_LOCATION)

# Logger初期化
search = Search()


def main():
    st.title("Search and Chat")
    option1 = 'Gemini Pro'
    option2 = 'PaLM (chat-bison@002)'
    option3 = '経済産業省レポート'
    option = st.selectbox(
    '知識DB',
    (option1, option2, option3))

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # React to user input
    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": prompt})

        
        if option == option1:
            # Execute Gemini
            res = gemini.chat(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(res.text, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": res.text})

            # ログに記録
            logger.send_log(user, option, prompt, res.text)

        if option == option2:
            # Execute PaLM API
            res = chat.chat(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(res.text, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": res.text})

            # ログに記録
            logger.send_log(user, option, prompt, res.text)

        elif option == option3:
            res = search.search(PROJECT_ID, LOCATION, DATA_STORE_ID, prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(res.summary.summary_text, unsafe_allow_html=True)
                for item in res.results:
                    dict = MessageToDict(item.document._pb)
                    link = dict['derivedStructData']['link'].replace("gs://", "https://storage.googleapis.com/")
                    st.link_button(dict['derivedStructData']['title'], link)
            st.session_state.messages.append({"role": "assistant", "content": res.summary.summary_text})

            # ログに記録
            logger.send_log(user, option, prompt, res.summary.summary_text)

if __name__ == "__main__":
    main()