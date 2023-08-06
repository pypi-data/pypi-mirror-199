from .base import BaseModel

class UpdateApiRequest(BaseModel):
    def __init__(self, name: str=None, version: str=None):
        """
Initialize UpdateApiRequest 
Parameters:
----------
    name: str
    version: str
        """
        if name is not None:
            self.name= name
        if version is not None:
            self.version= version