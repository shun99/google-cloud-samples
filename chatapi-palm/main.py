from typing import Any, Mapping
from verify_token import verify_id_token
from chat import Chat
from logger import Logger
import os
import flask
import functions_framework

e = os.environ
SKIP_VERIFICATION = e.get("SKIP_VERIFICATION")
PROJECT_ID = e.get("GOOGLE_CLOUD_PROJECT")
PROJECT_NUMBER = e.get("PROJECT_NUMBER")
MODEL_LOCATION = e.get("MODEL_LOCATION", "us-central1")

chat = Chat(PROJECT_ID, MODEL_LOCATION)
logger = Logger()

@functions_framework.http

def hello_chat(req: flask.Request) -> Mapping[str, Any]:
  
  if SKIP_VERIFICATION != "True":
    # ヘッダーよりAuthorizationを取得
    auth_header = flask.request.headers.get('Authorization')

    # Bear tokenの取得
    if auth_header:
        bearer_token = auth_header.split(' ')[1]  # Authorization: Bearer <token>
    else:
        print('Invalid token')
        return flask.abort(403)

    # tokenの検証
    verify_id_token(PROJECT_NUMBER, bearer_token)
  
  request_json = req.get_json(silent=True)
  if request_json:
    prompt = (request_json["message"]["text"])
    event_time = (request_json["eventTime"])
    user = (request_json["message"]["sender"]["email"])
  else:
    prompt = "Hi!"
    event_time = "yyyy/mm/dd"
    user = "Test User"

  # PaLM API実行
  res = chat.chat(prompt)

  # 応答をChat形式に変更
  chat_response = {
    "text": res.text
  }

  # ログに記録
  logger.send_log(event_time, user, prompt, res.text)

  return chat_response
  
