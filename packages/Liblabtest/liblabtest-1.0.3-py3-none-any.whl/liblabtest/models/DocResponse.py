from .base import BaseModel

class DocResponse(BaseModel):
    def __init__(self, previewUrl: str, previewSlug: str, artifactId: float, version: str, fileLocation: str, updatedAt: str, createdAt: str, id: float):
        """
Initialize DocResponse 
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
        self.previewUrl= previewUrl
        self.previewSlug= previewSlug
        self.artifactId= artifactId
        self.version= version
        self.fileLocation= fileLocation
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id