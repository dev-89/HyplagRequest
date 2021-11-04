import time
import requests
import jwt

class JwtToken():
  host : str
  name : str
  secret : str
  access_token : str
  exp : str

  def __init__(self, host : str, name : str, secret : str) -> None:
    self.host = host
    self.name = name
    self.secret = secret
    self.exp = time.time()

    try:
      self.access_token = self.get_access_token()
      if self.access_token is None:
        raise Exception("Request for access token failed.")
    except Exception as e:
      print(e)

  def update_exp(self, token : str) -> None:
    decoded = jwt.decode(token, options={"verify_signature": False})
    self.exp = decoded['exp']

  def get_access_token(self) -> str:
    try:
      token_body = {
        "name": self.name,
        "password": self.secret
      }
      request = requests.post(self.host+"/token/create", json=token_body)
      request.raise_for_status()
      token = request.json()['token']
      self.update_exp(token)
      return token
    except Exception as e:
      print(e)
      return None