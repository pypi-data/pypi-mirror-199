from .base import BaseModel

class CreateDocRequest(BaseModel):
    def __init__(self, previewSlug: str, apiId: float, artifactId: float, version: str, fileLocation: str):
        """
Initialize CreateDocRequest 
Parameters:
----------
    previewSlug: str
    apiId: float
    artifactId: float
    version: str
    fileLocation: str
        """
        self.previewSlug= previewSlug
        self.apiId= apiId
        self.artifactId= artifactId
        self.version= version
        self.fileLocation= fileLocation