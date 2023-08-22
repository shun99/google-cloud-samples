import sys
from oauth2client import client

def verify_id_token(token):
  # Project番号を指定してください
  audience = '511748666295'

  # Bearerトークン発行元
  chat_issuer = 'chat@system.gserviceaccount.com'

  # 検証Url
  public_cert_url_prefix = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

  # Bearerトークン
  # ヘッダーで'Authorization: Bearer AbCdEf123456'であれば'AbCdEf123456'.
  bearer_token = token

  # トークン検証実行
  try:
    token = client.verify_id_token(bearer_token, audience, cert_uri=public_cert_url_prefix + chat_issuer)

    if token['iss'] != chat_issuer:
      sys.exit('Invalid issuee')
  except:
    sys.exit('Invalid token')

  # トークンが有効
  print('The token is valid')