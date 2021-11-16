import requests
import json
import logging
import aiohttp
import asyncio
import time
import jwt
import os
from  urllib.parse import urlencode

from requests_toolbelt.multipart.encoder import MultipartEncoder
from pathlib import Path

from .settings import HyplagConfig
from .exceptions import ResultNotReadyException

class AsyncRequest():

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

  async def send_json_request(self, session, url, json, verb, params=None):
    url = self.config.token.host + url
    async with session.request(
      method=verb, 
      url=url, 
      json=json, 
      params=params,
      headers={'Authorization': f'Bearer {self.config.token.access_token}'}) as resp:
      data = await resp.read()
      return data

  async def send_header_request(self, session, url, verb, params=None):
    async with session.request(
      method=verb, 
      url=self.config.token.host+url, 
      params=params,
      headers={
        'Authorization': f'Bearer {self.config.token.access_token}'
      }) as resp:
      data = await resp.json()
      code = resp.status
      if code == 303:
        raise ResultNotReadyException
      return data

  def send_file(self, filepath):
    url = self.config.token.host + f'/indexing'
    filename = Path(filepath).name
    mp_encoder = MultipartEncoder(
      fields={
          'external_id': 'Request',
          'multipartFile': (filename, open(filepath, 'rb'),'application/pdf')
      }
    )
    response = requests.Session().post(
      url, 
      data=mp_encoder,
      headers={'Content-Type': mp_encoder.content_type,
      'Authorization': f'Bearer {self.config.token.access_token}'}
    )
    return response.text

  @Decorators.refreshToken
  async def send_single_json_request(self, url, json, verb='POST', params=None):
    async with aiohttp.ClientSession() as session:
      response = await self.send_json_request(session, url, json, verb, params=params)
      return response

  @Decorators.refreshToken
  async def send_multiple_json_requests(self, url, json_list, verb='POST', params=None):
    async with aiohttp.ClientSession() as session:
      tasks = []
      for json in json_list:
        tasks.append(asyncio.ensure_future(self.send_json_request(session, url, json, verb, params)))
      responses = await asyncio.gather(*tasks)
      return json.loads(responses)

  @Decorators.refreshToken
  async def send_single_header_request(self, url, verb='POST', params=None):
    async with aiohttp.ClientSession() as session:
      response = await self.send_header_request(session, url, verb, params)
      return response

  @Decorators.refreshToken
  async def send_multiple_header_requests(self, urls, verb='POST', params=None):
    async with aiohttp.ClientSession() as session:
      tasks = []
      for url in urls:
        tasks.append(asyncio.ensure_future(self.send_header_request(session, url, verb, params)))
      responses = await asyncio.gather(*tasks)
      return responses

  @Decorators.refreshToken
  def send_single_file(self, filepath):
    response = self.send_file(filepath)
    return json.loads(response)