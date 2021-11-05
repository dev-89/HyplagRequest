import logging
import asyncio

from .async_request import AsyncRequest
from .settings      import HyplagConfig
from .datastructures.datastructures import *
from .exceptions import ResultNotReadyException

def returned_typed_list(data_list, class_type):
  return_list = []
  for data in data_list:
    if isinstance(data, list):
      sublist = []
      for subdata in data:
        sublist.append(class_type.parse_obj(subdata))
      return_list.append(sublist)
    else:
      return_list.append(class_type.parse_obj(data))
  return return_list

class HyplagRequest:
  def __init__(self, credentials=None):
    self.config = HyplagConfig()
    self.config.setup(credentials=credentials)
    self.request = AsyncRequest(self.config)
    self.logger = logging.getLogger(__name__)

  def retrieve_algorithms(self):
    result = self.request.send_single_header_request('/algorithm')
    return returned_typed_list(result, AlgorithmStrcture)

  def get_document_info(self, id):
    result = asyncio.run(self.request.send_single_header_request('/document/' + str(id), verb='GET'))
    return HyplagDocument.parse_obj(result)

  def get_multiple_document_info(self, ids):
    urls = ['/document/' + str(id) for id in ids]
    result = asyncio.run(self.request.send_multiple_header_requests(urls, verb='GET'))
    return returned_typed_list(result, HyplagDocument)

  def get_document_authors(self, id):
    result = asyncio.run(self.request.send_multiple_header_requests('/document/' + str(id) + '/authors', verb='GET'))
    return Author.parse_obj(result)

  def get_multiple_document_authors(self, ids):
    urls = ['/document/' + str(id) + '/authors' for id in ids]
    result = asyncio.run(self.request.send_multiple_header_requests(urls, verb='GET'))
    return returned_typed_list(result, Author)

  def get_document_authors(self, id) -> dict:
    result = asyncio.run(self.request.send_multiple_header_requests('/document/' + str(id) + '/authors', verb='GET'))
    return Author.parse_obj(result)
  
  def get_analysis_result(self, id):
    result = asyncio.run(self.request.send_multiple_header_requests('/result/' + str(id), verb='GET'))
    return Results.parse_obj(result)

  def is_analysis_ready(self, id) -> bool:
    try:
      asyncio.run(self.request.send_multiple_header_requests('/result/' + str(id), verb='GET'))
    except ResultNotReadyException:
      return False
    return True

  def submit_analysis(self, source_document_id, available_algorithms) -> int:
    params = {
      "external_id": 'recvis',
      "resultTimeout": 0
    }

    body = {
      "algorithmIds": available_algorithms,
      "scopes": ["0"],
      "sourceDocumentId": source_document_id
    }
    result = asyncio.run(self.request.send_single_json_request('/detection', json=body, verb='POST', params=params))
    return result

  def send_document(self, file_path) -> int:
    result = self.request.send_single_file(file_path)
    return result

  def get_algorithm_result(self, json) -> dict:
    result = asyncio.run(self.request.send_single_json_request('/result/' + str(id), json=json, verb='GET'))
    return result