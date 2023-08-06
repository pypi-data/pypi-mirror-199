from .base import BaseModel
class ArtifactType(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class CreateArtifactRequest(BaseModel):
    def __init__(self, bucketKey: str, bucketName: str, buildId: float, artifactType: ArtifactType):
        """
Initialize CreateArtifactRequest 
Parameters:
----------
    bucketKey: str
    bucketName: str
    buildId: float
    artifactType: ArtifactType
        """
        self.bucketKey= bucketKey
        self.bucketName= bucketName
        self.buildId= buildId
        self.artifactType= artifactType