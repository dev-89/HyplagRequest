"""
This script uploads a file defined in 'pathToPdf' and uploads it to the Hyplag backend. The data of the hyplag backend are given in the .env file. After uploading the full document data and authors are
retrieved from the uploaded file.
"""

from hyplagrequest import HyplagRequest

pathToPdf = '/path/to/file.pdf'

hyRequest = HyplagRequest()
response = hyRequest(
  _uploadDocument=pathToPdf, # file to upload
  _getDocumentFullData = -1, # return full data of uploaded file
  _getDocumentAuthors = -1   # get authors of 
)

print(response)