from pydantic import BaseModel
from typing import List, Dict, Optional

class AlgorithmStrcture(BaseModel):
  id: str
  description: str
  retrievalStage: str
  similarityFeature: str
  resultFormat: str
  significance: int

class ResultConfiguration(BaseModel):
  algorithmIds: List[str]
  scopes: Optional[List[str]]
  selectedDocumentIds: Optional[List[int]]
  sourceDocumentId: int

class Results(BaseModel):
  configuration: ResultConfiguration
  endDate: str
  findings: Dict[str, List[int]]
  resultDataId: str
  startDate: str

class HyplagImages(BaseModel):
  imageId: str
  inBody: bool
  name: str
  ordinal: int
  teiId: str

class HyplagDocument(BaseModel):
  accountId: int
  authorIds: List[int]
  contentBody: str
  contentTxtHash: int
  documentId: int
  expirationDate: Optional[str]
  images: List[HyplagImages]
  importDate: str
  lastModified: str
  mimeType: str
  originalFieldName: Optional[str]
  originalFileReference: Optional[str]
  pubDate: Optional[str]
  referenceIds: List[int]
  scopes: List[str]
  title: str
  userId: str

class Author(BaseModel):
  authorId: int
  name: str
  surname: str