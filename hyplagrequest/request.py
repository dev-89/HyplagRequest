import requests
import logging
import time
import shlex
import subprocess

from urllib.parse import urljoin
from typing import Tuple

from .settings import HyplagConfig

def call_curl(curl):
    args = shlex.split(curl)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr

class Request():

  class Decorators():
    @staticmethod
    def refreshToken(decorated):
        def wrapper(api, *args, **kwargs):
            if time.time() > api.config.token.exp:
                api.config.token.get_access_token()
            return decorated(api, *args, **kwargs)
        return wrapper

  def __init__(self, hyplagConfig: HyplagConfig) -> None:
    self.logger = logging.getLogger(__name__)
    self.config = hyplagConfig

  @Decorators.refreshToken
  def send_json_request(self, url: str, json: dict, verb:str, params: str = None) -> Tuple[int, str]:
      url = urljoin(self.config.token.host, url)
      resp = requests.request(
          method=verb,
          url=url,
          json=json,
          params=params,
          headers={'Authorization': f'Bearer {self.config.token.access_token}'
          })
      resp.raise_for_status()
      return resp.status_code, resp.text

  @Decorators.refreshToken
  def send_header_request(self, url: str, verb: str, params: str = None) -> Tuple[int, str]:
      url = urljoin(self.config.token.host, url)
      resp = requests.request(
          method=verb,
          url=url,
          params=params,
          headers={
            'Authorization': f'Bearer {self.config.token.access_token}'
          })
      resp.raise_for_status()
      return resp.status_code, resp.text

  @Decorators.refreshToken
  def send_file(self, filepath: str) -> Tuple[int, str]:
    url = urljoin(self.config.token.host, '/indexing')

    cmd = f"""curl -L -X POST \"{url}?external_id={self.config.external_id}&scopes=0&mimeType=PDF\" 
    -H \"Authorization: Bearer {self.config.token.access_token}\" 
    -H \"Content-Type: multipart/form-data\" 
    -H 'Accept: application/json' 
    -F multipartFile=@{filepath}"""
    stdout, stderr = call_curl(cmd)
    return stdout, stderr
