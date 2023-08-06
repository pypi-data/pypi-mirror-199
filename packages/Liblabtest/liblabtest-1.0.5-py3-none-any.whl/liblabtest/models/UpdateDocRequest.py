from .base import BaseModel

class UpdateDocRequest(BaseModel):
    def __init__(self, fileLocation: str=None, version: str=None):
        """
Initialize UpdateDocRequest 
Parameters:
----------
    fileLocation: str
    version: str
        """
        if fileLocation is not None:
            self.fileLocation= fileLocation
        if version is not None:
            self.version= version