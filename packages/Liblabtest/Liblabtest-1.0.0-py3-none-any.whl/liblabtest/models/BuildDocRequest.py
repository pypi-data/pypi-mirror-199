from .base import BaseModel

class BuildDocRequest(BaseModel):
    def __init__(self, openApiUrl: str, apiId: float):
        """
Initialize BuildDocRequest 
Parameters:
----------
    openApiUrl: str
    apiId: float
        """
        self.openApiUrl= openApiUrl
        self.apiId= apiId