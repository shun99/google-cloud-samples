
from typing import Union, Dict, Optional
import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

class Chat:

    def __init__(self, 
                    project_id: Optional[str], 
                    model_location: Optional[str], 
                    params: Dict[str, Union[int,float]] = {}
                ):

        vertexai.init(project=project_id, location=model_location)
        self.chat_model = ChatModel.from_pretrained("chat-bison@002")
        self.parameters = {
            "candidate_count": 1,
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
        self.parameters.update(params)


    def chat(self, req: str):
        chat = self.chat_model.start_chat()
        response = chat.send_message(req, **self.parameters)
        return response