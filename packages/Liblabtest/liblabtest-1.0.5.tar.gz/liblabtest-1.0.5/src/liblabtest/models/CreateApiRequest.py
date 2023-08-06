from .base import BaseModel

class CreateApiRequest(BaseModel):
    def __init__(self, orgId: float, version: str, name: str):
        """
Initialize CreateApiRequest 
Parameters:
----------
    orgId: float
    version: str
    name: str
        """
        self.orgId= orgId
        self.version= version
        self.name= name