from .hyplagrequest import HyplagRequest

"""import logging
import inspect
import json

from .document   import HyplagDocument
from .reqestor   import Requestor
from .algorithms import HyplagAlgorithms
from .analysis   import HyplagAnalysis
from .settings   import HyplagConfig
from .util       import HyplagUtil

class HyplagRequest:

  def __init__(self) -> None:
    self.config = HyplagConfig()
    self.config.setup()
    self.requestor = Requestor(self.config)
    self.logger = logging.getLogger(__name__)

  def __call__(self, 
  _uploadDocument: str=None,
  _retrieveAlgorithms: bool = False,
  _retrieveAlgorithmsByType: str=None,
  _getDocumentAuthors: int = None,
  _getDocumentMetaData: int = None,
  _getDocumentFullData: int = None,
  _submitAnalysis: str = None,
  _isResultReady: int = None,
  _getAnalysisResult: int = None,
  _getAlgorithmResult: int = None,
  _documentIdsFromResult: dict = None,
  _resultsByDocumentId: dict = None,
  _resultDataStructure: dict = None,
  _structuredDocumentData: int = None,
  targetDocuments: list = None
  ) -> dict:
    returnHash = {}
    self.logger.info("Running HyplagRequest.")
    self.logger.debug("Selected parameters for request:")
    #self.logger.debug(inspect.getargspec(self.__call__))

    try:
      with self.requestor as hyplagSession:
        if _uploadDocument is not None:
          self.logger.info("HyplagRequest received: document %s to upload.", _uploadDocument)
          returnHash['documentID'] = self.uploadFile(_uploadDocument, hyplagSession)
          self.logger.info("Successfully loaded document %s to Hyplag with ID %s.", _uploadDocument, returnHash['documentID'])
          if returnHash['documentID'] is None:
            raise Exception("Error while uploading document.")

        if _retrieveAlgorithmsByType is not None:
          self.logger.info("HyplagRequest received: getting data of available algorithms for type: %s.", _retrieveAlgorithmsByType)
          algorithms = self.retrieveAlgorithms(hyplagSession)
          returnHash['algorithmDataOfType'] = algorithms.getAvailableAlgorithmsDataByType(_retrieveAlgorithmsByType)

        if _retrieveAlgorithms:
          self.logger.info("HyplagRequest received: getting list and data on available algorithms.")
          algorithms = self.retrieveAlgorithms(hyplagSession)
          returnHash['algorithmIDs'] = algorithms.AVAILABLE_ALGORITHMS_ID_LIST
          returnHash['algorithmData'] = algorithms.AVAILABLE_ALGORITHMS_DATA

        if _getDocumentAuthors is not None:
          toInt = int(_getDocumentAuthors)
          if toInt == -1:
            self.logger.info("HyplagRequest received: getting authors of uploaded document.")
            returnHash['documentAuthors'] = self.getDocumentAuthors(str(returnHash['documentID']), hyplagSession)
          elif toInt > 0:
            self.logger.info("HyplagRequest received: getting authors of document with ID %s.", _getDocumentAuthors)
            returnHash['documentAuthors'] = self.getDocumentAuthors(_getDocumentAuthors, hyplagSession)
          else:
            raise Exception("Invalid input for document ID to retrieve document authors.")

        if _getDocumentMetaData is not None:
          toInt = int(_getDocumentMetaData)
          if toInt == -1:
            self.logger.info("HyplagRequest received: getting metadata of uploaded document.")
            returnHash['documentMetaData'] = self.getDocumentMetaData(str(returnHash['documentID']), hyplagSession)
          elif toInt > 0:
            self.logger.info("HyplagRequest received: getting metadata of document with ID %s.", _getDocumentMetaData)
            returnHash['documentMetaData'] = self.getDocumentMetaData(_getDocumentMetaData, hyplagSession)
          else:
            raise Exception("Invalid input for document ID to retrieve document metadata.")

        if _getDocumentFullData is not None:
          toInt = int(_getDocumentFullData)
          if toInt == -1:
            self.logger.info("HyplagRequest received: getting full data of uploaded document.")
            returnHash['documentFullData'] = self.getDocumentFullData(returnHash['documentID'], hyplagSession)
          elif toInt > 0:
            self.logger.info("HyplagRequest received: getting full data of document with ID %s.", _getDocumentFullData)
            returnHash['documentFullData'] = self.getDocumentFullData(_getDocumentFullData, hyplagSession)
          else:
            raise Exception("Invalid input for document ID to retrieve document full data.")

        if _structuredDocumentData is not None:
          toInt = int(_structuredDocumentData)
          if toInt == -1:
            self.logger.info("HyplagRequest received: getting full data of uploaded document.")
            returnHash['documentFullData'] = self.getStructuredDocumentData(returnHash['documentID'], hyplagSession)
          elif toInt > 0:
            self.logger.info("HyplagRequest received: getting full data of document with ID %s.", _getDocumentFullData)
            returnHash['documentFullData'] = self.getStructuredDocumentData(_structuredDocumentData, hyplagSession)
          else:
            raise Exception("Invalid input for document ID to retrieve document full data.")

        if _submitAnalysis is not None:
          if _submitAnalysis == -1:
            self.logger.info("HyplagRequest received: submitting analysis of uploaded document.")
            returnHash['analysisID'] = self.submitAnalysis(returnHash['documentID'], hyplagSession)
          elif isinstance(_submitAnalysis, int):
            self.logger.info("HyplagRequest received: submitting analysis of document with ID %s.", _submitAnalysis)
            returnHash['analysisID'] = self.submitAnalysis(_submitAnalysis, hyplagSession)
          else:
            raise Exception("Invalid input for document ID to submit analysis.")

        if _isResultReady is not None:
          if _isResultReady == -1:
            self.logger.info("HyplagRequest received: checking if submitted analysis is ready.")
            returnHash['analysisReady'] = self.isResultReady(returnHash['analysisID'], hyplagSession)
          elif isinstance(_isResultReady, str):
            self.logger.info("HyplagRequest received: checking if analysis with ID %s is ready.", _isResultReady)
            returnHash['analysisReady'] = self.isResultReady(_isResultReady, hyplagSession)
          else:
            raise Exception("Invalid input for analysis ID to check if result is ready.")

        if _getAnalysisResult is not None:
          if _getAnalysisResult == -1:
            self.logger.info("HyplagRequest received: getting result of submitted analysis.")
            returnHash['analysisResult'] = self.getAnalysisResult(returnHash['analysisID'], hyplagSession)
          elif isinstance(_getAnalysisResult, str):
            self.logger.info("HyplagRequest received: getting result of analysis with ID %s.", _getAnalysisResult)
            returnHash['analysisResult'] = self.getAnalysisResult(_getAnalysisResult, hyplagSession)
          else:
            raise Exception("Invalid input for analysis ID to retrieve analysis result.")

        if _getAlgorithmResult is not None:
          self.logger.info("HyplagRequest received: getting result of submitted analysis.")
          returnHash['algorithmResult'] = self.getAlgorithmResult(_getAlgorithmResult, hyplagSession)
 
        if _documentIdsFromResult is not None:
          self.logger.info("HyplagRequest received: getting result of submitted analysis.")
          returnHash['documentIds'] = self.getDocumentIdsFromResult(_documentIdsFromResult)

        if _resultDataStructure is not None:
          self.logger.info("HyplagRequest received: getting result of analysis with ID %s.", _getAnalysisResult)
          returnHash['dataStructure'] = self.analysisDataStructure(_resultDataStructure)

        if _resultsByDocumentId is not None:
          self.logger.info("HyplagRequest received: getting result of analysis with ID %s.", _getAnalysisResult)
          returnHash['resultsById'] = self.resultsByDocumentId(_resultsByDocumentId)

        return returnHash
    except Exception as e:
      self.logger.error(e)
      raise e

  def uploadFile(self, filePath, hyplagSession):
    uploadDocument = HyplagDocument(hyplagSession)
    docID = uploadDocument.sendDocumentToHyplag(filePath)
    return docID
  
  def retrieveAlgorithms(self, hyplagSession) -> HyplagAlgorithms:
    algorithms = HyplagAlgorithms(hyplagSession)
    algorithms()
    return algorithms

  def getDocumentAuthors(self, documentID, hyplagSession):
    document = HyplagDocument(hyplagSession)
    authors = document.getDocumentAuthors(documentID)
    return authors

  def getDocumentMetaData(self, documentID, hyplagSession):
    document = HyplagDocument(hyplagSession)
    metaData = document.getDocumentMetadata(documentID)
    return metaData

  def getDocumentFullData(self, documentID, hyplagSession):
    document = HyplagDocument(hyplagSession)
    fullData = document.getDocumentFullData(documentID)
    return fullData

  def getStructuredDocumentData(self, documentID, hyplagSession):
    document = HyplagDocument(hyplagSession)
    fullData = document.getStructuredDocumentData(documentID)
    return fullData

  def submitAnalysis(self, sourceDocumentID, hyplagSession):
    algorithms = HyplagAlgorithms(hyplagSession)
    algorithms()
    availableAlgorithms = algorithms.AVAILABLE_ALGORITHMS_ID_LIST
    analysis = HyplagAnalysis(hyplagSession)
    analysisID = analysis.submitAnalysis(sourceDocumentID, availableAlgorithms)
    return analysisID

  def isResultReady(self, analysisID, hyplagSession):
    analysis = HyplagAnalysis(hyplagSession)
    readyStatus = analysis.isResultReady(analysisID)
    return readyStatus

  def getAnalysisResult(self, analysisID, hyplagSession):
    analysis = HyplagAnalysis(hyplagSession)
    response = analysis.getAnalysisResult(analysisID)
    return response

  def getAlgorithmResult(self, jsonData, hyplagSession):
    analysis = HyplagAnalysis(hyplagSession)
    response = analysis.getAlgorithmsResult(jsonData)
    return response

  def analysisDataStructure(self, resultData):
    util = HyplagUtil()
    response = util.algorithm_data_structure(resultData)
    return response

  def resultsByDocumentId(self, resultData):
    util = HyplagUtil()
    response = util.get_results_by_document_id(resultData)
    return response

  def getDocumentIdsFromResult(self, resultData):
    util = HyplagUtil()
    response = util.retrieve_document_ids_from_results(resultData)
    return response

  def is_json(self, myjson):
    try:
      json_object = json.loads(myjson)
    except ValueError as e:
      return False
    return True
"""