from typing import Any, Mapping
from verify_token import verify_id_token
from chat import chat
import os
import flask
import functions_framework

@functions_framework.http

def hello_chat(req: flask.Request) -> Mapping[str, Any]:
  
  if os.environ.get("SKIP_VERIFICATION", "False") != "True":
    # ヘッダーよりAuthorizationを取得
    auth_header = flask.request.headers.get('Authorization')

    # Bear tokenの取得
    if auth_header:
        bearer_token = auth_header.split(' ')[1]  # Authorization: Bearer <token>
    else:
        print('Invalid token')
        return flask.abort(403)

    # tokenの検証
    verify_id_token(bearer_token)
  
  request_json = req.get_json(silent=True)
  if request_json:
    text = (request_json["message"]["text"])
  else:
    text = "Hi!"

  # PaLM API実行
  res = chat(text)

  # 応答をChat形式に変更
  chat_response = {
    "text": res.text
  }

  return chat_response
  
