from typing import Union, Dict, Optional
from google.cloud import logging

class Logger:
    def __init__(self,params: Dict[str, Union[int,float]] = {}):

        # cloud logging
        self.logging_client = logging.Client()

        # cloud logging: 書き込むログの名前
        self.logger_name = "palm_chat"
        
        # cloud logging: ロガーを選択する
        self.logger = self.logging_client.logger(self.logger_name)
    
    def send_log(self, event_time: str, user_id: str, prompt: str, payload: str) -> None:
        # ログに書き込むデータを持つ辞書を作成する
        data = {
            "event_time": event_time,
            "user": user_id,
            "prompt": prompt,
            "response": payload,
            "type": "history",
        }
    
        # 辞書をJSON文字列に変換する
        self.logger.log_struct(data)
