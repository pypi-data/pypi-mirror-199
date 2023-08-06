from .base import BaseModel
from enum import Enum
class Language(Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    TYPESCRIPT = "TYPESCRIPT"
    def list():
        return list(map(lambda x: x.value, Language._member_map_.values()))
class SdkResponse(BaseModel):
    def __init__(self, artifactId: float, version: str, fileLocation: str, language: Language, updatedAt: str, createdAt: str, id: float):
        """
Initialize SdkResponse 
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
        self.artifactId= artifactId
        self.version= version
        self.fileLocation= fileLocation
        self.language = self._enum_matching(language, Language.list(), "language")
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id