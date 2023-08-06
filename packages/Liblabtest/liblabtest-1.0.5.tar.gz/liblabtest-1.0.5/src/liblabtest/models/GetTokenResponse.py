from .base import BaseModel
from typing import List
class GetTokenResponseScope(BaseModel):
    def __init__(self):        pass

class GetTokenResponse(BaseModel):
    def __init__(self, scope: List[GetTokenResponseScope], expiresAt: str, name: str, id: float):
        """
Initialize GetTokenResponse 
Parameters:
----------
    scope: list of GetTokenResponseScope
    expiresAt: str
    name: str
    id: float
        """
        self.scope= scope
        self.expiresAt= expiresAt
        self.name= name
        self.id= id