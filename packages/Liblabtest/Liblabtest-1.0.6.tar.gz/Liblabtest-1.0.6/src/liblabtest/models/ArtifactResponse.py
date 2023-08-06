from __future__ import annotations
from .base import BaseModel
from enum import Enum
from .DocResponse import DocResponse
from .SdkResponse import SdkResponse




class Status(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"
    def list():
        return list(map(lambda x: x.value, Status._member_map_.values()))

class ArtifactType(Enum):
    SDK = "SDK"
    DOC = "DOC"
    LOG = "LOG"
    ZIP = "ZIP"
    SPEC = "SPEC"
    def list():
        return list(map(lambda x: x.value, ArtifactType._member_map_.values()))

class Doc(DocResponse):
    def __init__(self, id:float,createdAt:str,updatedAt:str,fileLocation:str,version:str,artifactId:float,previewSlug:str,previewUrl:str, ):
        """
Initialize Doc 
Parameters:
----------
    previewUrl: str
    previewSlug: str
    artifactId: float
    version: str
    fileLocation: str
    updatedAt: str
    createdAt: str
    id: float
        """

        DocResponse.__init__(self, **{"id": id,"createdAt": createdAt,"updatedAt": updatedAt,"fileLocation": fileLocation,"version": version,"artifactId": artifactId,"previewSlug": previewSlug,"previewUrl": previewUrl})

class Sdk(SdkResponse):
    def __init__(self, id:float,createdAt:str,updatedAt:str,language:str,fileLocation:str,version:str,artifactId:float, ):
        """
Initialize Sdk 
Parameters:
----------
    artifactId: float
    version: str
    fileLocation: str
    language: str
    updatedAt: str
    createdAt: str
    id: float
        """

        SdkResponse.__init__(self, **{"id": id,"createdAt": createdAt,"updatedAt": updatedAt,"language": language,"fileLocation": fileLocation,"version": version,"artifactId": artifactId})
class ArtifactResponse(BaseModel):
    def __init__(self, bucketKey: str, bucketName: str, error: str, status: Status, buildId: float, artifactUrl: str, artifactType: ArtifactType, updatedAt: str, createdAt: str, id: float, doc: Doc=None, sdk: Sdk=None):
        """
Initialize ArtifactResponse 
Parameters:
----------
    bucketKey: str
    bucketName: str
    error: str
    status: str
    buildId: float
    artifactUrl: str
    artifactType: str
    updatedAt: str
    createdAt: str
    id: float
    doc: Doc
    sdk: Sdk
        """
        self.bucketKey= bucketKey
        self.bucketName= bucketName
        self.error= error
        self.status = self._enum_matching(status, Status.list(), "status")
        self.buildId= buildId
        self.artifactUrl= artifactUrl
        self.artifactType = self._enum_matching(artifactType, ArtifactType.list(), "artifactType")
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id
        if doc is not None:
            self.doc= doc
        if sdk is not None:
            self.sdk= sdk