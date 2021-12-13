import logging
import json

from typing import Union

from .request                       import Request
from .settings                      import HyplagConfig
from .datastructures.datastructures import *
from .exceptions                    import HyplagRequestException
from .status_codes                  import HttpStatusCode

class HyplagRequest:
  def __init__(self, credentials: dict):
    """this is the main class communiating with the HyPlag backend through a 
    RESTful API. Use this class to make requests to HyPlag and receive typed
    responses.
    
    Keyword arguments:
    credentials -- structure of dict: {host: 'host-url', user: 'username', password: 'userpass'} 
    """
    
    self.config = HyplagConfig()
    self.config.setup(credentials=credentials)
    self.request = Request(self.config)
    self.logger = logging.getLogger(__name__)

  def retrieve_algorithms(self):
    try:
        _, result = self.request.send_header_request('/algorithm', verb='GET')
        result = json.loads(result)
        typed_result = [AlgorithmStrcture(**algorithm_dict) for algorithm_dict in result]
        return typed_result
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def retrieve_algorithm_ids(self):
    try:
        _, result = self.request.send_header_request('/algorithm', verb='GET')
        result = json.loads(result)
        id_list = [id['id'] for id in result]
        return id_list
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def get_document_info(self, id):
    try:
        _, result = self.request.send_header_request('/document/' + str(id), verb='GET')
        result = json.loads(result)
        return HyplagDocument(**result)
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def get_document_authors(self, id):
    try:
        _, result = self.request.send_header_request('/document/' + str(id) + '/authors', verb='GET')
        result = json.loads(result)
        typed_result = [Author(**algorithm_dict) for algorithm_dict in result]
        return typed_result
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def get_analysis_result(self, id) -> Union[bool, Results]:
    try:
        code, result = self.request.send_header_request('/result/' + str(id), verb='GET')
        result = json.loads(result)
        if code == HttpStatusCode.SEE_OTHER:
            return None
        return Results(**result)
    except Exception as e:
        print(e)
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def is_analysis_ready(self, id) -> bool:
    try:
        code, _ = self.request.send_header_request('/result/' + str(id), verb='GET')
        if code == HttpStatusCode.SEE_OTHER:
            return False
        return True
    except:
        return False

  def submit_analysis(self, source_document_id : int, available_algorithms : List[str], scopes: List[str] = ["0"], result_timeout : int = 0) -> str:
    params = {
      "external_id": self.config.external_id,
      "resultTimeout": result_timeout
    }

    body = {
      "algorithmIds": available_algorithms,
      "scopes": scopes,
      "sourceDocumentId": source_document_id
    }
    try:
        _, result = self.request.send_json_request('/detection', json=body, verb='POST', params=params)
        return result
    except Exception as e:
        print(e)
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def send_document(self, file_path) -> int:
    try:
        code, _ = self.request.send_file(file_path)
        if code.isnumeric():
            return int(code)
        else:
            json_data = json.loads(code)
            return json_data['context']['documentId']
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None

  def get_algorithm_result(self, json) -> dict:
    try:
        _, result = self.request.send_json_request('/result/algorithms', json=json, verb='POST')
        return result
    except Exception as e:
        raise HyplagRequestException("An error occureed while making a request to Hyplag backend") from None
