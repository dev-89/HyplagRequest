"""
This script is a Recvis style similarity analysis. It is assumed that the source document 
and at least 
"""
import time

from os import wait

from hyplagrequest import HyplagRequest

sourceDocument = 15 # Replace with IDs
targetDocuments = [12, 13, 14]
similarityThreshold = 0.1
maximumDocumentCount = 5


class SimilarityModel():

  @staticmethod
  def getGlobalSimilarityValue(matchedDocumentData):
    return SimilarityModel.calculateGlobalSimilarityValue(
      matchedDocumentData['similarities']['text'],
      matchedDocumentData['similarities']['citation'],
      matchedDocumentData['similarities']['image'],
      matchedDocumentData['similarities']['formula']
    )

  @staticmethod
  def calculateGlobalSimilarityValue(
    textSimilarity, 
    citationSimilarity, 
    imageSimilarity, 
    formulaSimilarity
  ):
    return (textSimilarity+citationSimilarity+imageSimilarity+formulaSimilarity)/4

  def getSortedViaGlobalSimilarityValueWithMaxNumberOfDocuments(matchedDocumentsList, maxNumberOfDocuments):
    sorted(matchedDocumentsList, SimilarityModel.getGlobalSimilarityValue)
    return matchedDocumentsList[:maxNumberOfDocuments]


def calculateSimularity(
  algorithmType, 
  similarityMultiplierFactor, 
  paperID,
  structuredPaperAlgorithmResults, 
  matchedDocumentData):
    hyRequest = HyplagRequest()

    typeAlgorithms = hyRequest(
      _retrieveAlgorithmsByType=algorithmType
    )
    typeAlgorithms = typeAlgorithms['algorithmDataOfType']

    numAlgorithms = len(typeAlgorithms)
    if numAlgorithms == 0 or not structuredPaperAlgorithmResults:
      matchedDocumentData['similarities']['algorithmType'] = 0
      return
      
    algorithmsSimilaritySum = 0
    algorithmSignificanceSum = 0

    for algorithm in typeAlgorithms:
      algorithmId = algorithm['id']
      algorithmSignificance = algorithm['significance']

      algorithmSignificanceSum = algorithmSignificanceSum + algorithmSignificance
      if algorithmId == structuredPaperAlgorithmResults[paperID]['algorithmId']:
        currentSimilarityValue = structuredPaperAlgorithmResults[paperID]['value']
        algorithmsSimilaritySum = algorithmsSimilaritySum + currentSimilarityValue * algorithmSignificance

    matchedDocumentData['similarities'][algorithmType] = algorithmsSimilaritySum / algorithmSignificanceSum * similarityMultiplierFactor

def getMatchedAuthors(authorListToCheck, referenceAuthorList):
  authorMatchList = []
  for author in authorListToCheck:
    for referenceAuthor in referenceAuthorList:
      if author.lower() == referenceAuthor.lower():
        authorMatchList.append(author)
  return authorMatchList

hyRequest = HyplagRequest()

submitAnalysisResponse = hyRequest(
  _submitAnalysis=sourceDocument
)

# wait until Hyplag computed the results
response = hyRequest(
  _isResultReady=submitAnalysisResponse['analysisID']
)
while(not response['analysisReady']):
  response = hyRequest(
    _isResultReady=submitAnalysisResponse['analysisID']
  )
  print("waiting 1 sec")
  time.sleep(1)

analysisResult = hyRequest(
  _getAnalysisResult=submitAnalysisResponse['analysisID']
)

algorithmResultFeedData = hyRequest(
  _resultDataStructure = analysisResult['analysisResult']
)

algorithmResultFeedData['dataStructure']['targetDocumentIds'] = targetDocuments

algorithmResults = hyRequest(
  _getAlgorithmResult = algorithmResultFeedData['dataStructure']
)

matchedDocumentIDList = hyRequest(
  _documentIdsFromResult = algorithmResults
)

algorithmResults['completeDocumentIDList'] = matchedDocumentIDList['documentIds']

structuredPaperAlgorithmResults = hyRequest(
  _resultsByDocumentId = algorithmResults
)

structuredPaperAlgorithmResults = structuredPaperAlgorithmResults['resultsById']

paperMetaDataList = []
for documentId in targetDocuments:

  strcturedData = hyRequest(
    _structuredDocumentData = documentId
  )
  paperMetaDataList.append(strcturedData['documentFullData'])

sourceDocMetaData = hyRequest(
  _structuredDocumentData = sourceDocument
)

sourceDocMetaData = sourceDocMetaData['documentFullData']

sourceDocumentData = {
  "name": sourceDocMetaData['title'],
  "authors": [],
  "journal": sourceDocMetaData['journal'],
  "year": sourceDocMetaData['year'],
  "documentId": sourceDocument,
  "hyplagIdForSourceDoc": sourceDocMetaData['documentId']
}

for author in sourceDocMetaData['authors']:
  sourceDocumentData['authors'].append(author['name'] + ' ' + author['surname'])

for paperMetaData in paperMetaDataList:
  paperId = paperMetaData['documentId']
  matchedDocumentData = {
    "name": paperMetaData['title'],
    "authors": [],
    "journal": paperMetaData['journal'],
    "year": paperMetaData['year'],
    "similarities": {
      "text": 0,
      "citation": 0,
      "image": 0,
      "formula": 0,
    },
    "isCollected": False,
    "authorMatches": [],
    "isThereAuthorMatch": False,
    "documentId": paperMetaData['documentId']
  }
  for author in paperMetaData['authors']:
    matchedDocumentData['authors'].append(author['name'] + ' ' + author['surname'])

  algorithmKeys = ['text', 'citation', 'image', 'formula']

  similarityMultiplierFactor = 100.0

  matchedDocumentList = []

  for algorithmKey in algorithmKeys:

    calculateSimularity(
      algorithmKey,
      similarityMultiplierFactor,
      matchedDocumentData['documentId'],
      structuredPaperAlgorithmResults,
      matchedDocumentData
    )

  matchedDocumentData['authorMatches'] = getMatchedAuthors(matchedDocumentData['authors'], sourceDocumentData['authors'])
  matchedDocumentData['isThereAuthorMatch'] = len(matchedDocumentData['authorMatches']) > 0

  similarityValue = SimilarityModel.getGlobalSimilarityValue(matchedDocumentData)

  if similarityValue >= similarityThreshold:
    matchedDocumentList.append(matchedDocumentData)

  if len(matchedDocumentList) > maximumDocumentCount:
    matchedDocumentList = SimilarityModel.getSortedViaGlobalSimilarityValueWithMaxNumberOfDocuments(matchedDocumentList, maximumDocumentCount)

data = {
  'sourceDoc': sourceDocumentData,
  'matchedDocs': matchedDocumentList
}

print(data)