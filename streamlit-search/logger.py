import datetime
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
    
    def send_log(self, user_id: str, reference: str, prompt: str, payload: str) -> None:
        # 現在の日付と時刻を取得
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # ログに書き込むデータを持つ辞書を作成する
        data = {
            "event_time": formatted_datetime,
            "user": user_id,
            "reference": reference,
            "prompt": prompt,
            "response": payload,
            "type": "history",
        }
    
        # ログ書き込み
        self.logger.log_struct(data)