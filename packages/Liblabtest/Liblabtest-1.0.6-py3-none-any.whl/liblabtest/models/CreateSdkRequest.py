from .base import BaseModel
class Language(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class CreateSdkRequest(BaseModel):
    def __init__(self, artifactId: float, version: str, fileLocation: str, language: Language):
        """
Initialize CreateSdkRequest 
Parameters:
----------
    artifactId: float
    version: str
    fileLocation: str
    language: Language
        """
        self.artifactId= artifactId
        self.version= version
        self.fileLocation= fileLocation
        self.language= language