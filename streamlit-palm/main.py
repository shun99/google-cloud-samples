import streamlit as st
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import os

e = os.environ
PROJECT_ID = e.get("GOOGLE_CLOUD_PROJECT")
MODEL_LOCATION = e.get("MODEL_LOCATION", "asia-northeast1")

if "messages" not in st.session_state:
    st.session_state.messages = []

def chat(req: str):
    vertexai.init(project=PROJECT_ID, location=MODEL_LOCATION)
    chat_model = ChatModel.from_pretrained("chat-bison")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat(
        context="""""",
    )
    response = chat.send_message(req, **parameters)
    return response
    
def main():
    st.title("PaLM Chat")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Execute PaLM API
        res = chat(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(res.text)
        st.session_state.messages.append({"role": "assistant", "content": res.text})

if __name__ == "__main__":
    main()