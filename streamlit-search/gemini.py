from typing import Union, Dict, Optional
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

class Gemini:

    def __init__(self, 
                    project_id: Optional[str], 
                    model_location: Optional[str], 
                    config: Dict[str, Union[int,float]] = {}
                ):

        vertexai.init(project=project_id, location=model_location)
        self.config = {
            "max_output_tokens": 2048,
            "temperature": 0.9,
            "top_p": 1
        }
        self.model = GenerativeModel("gemini-pro")
        self.config.update(config)


    def chat(self, req: str):
        chat = self.model.start_chat()
        response = chat.send_message(req, generation_config=self.config)
        return response