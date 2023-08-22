import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

# Project IDを指定してください
project_id = "<Project ID>"
location = "us-central1"

vertexai.init(project=project_id, location=location)
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 1024,
    "top_p": 0.8,
    "top_k": 40
}

def chat(req):
    chat = chat_model.start_chat()
    response = chat.send_message(req, **parameters)
    return response