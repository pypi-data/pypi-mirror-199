from .base import BaseModel
from typing import List
from enum import Enum
class CreateTokenRequestScope(Enum):
    SDK = "SDK"
    DOC = "DOC"
    BUILD = "BUILD"
    API = "API"
    ARTIFACT = "ARTIFACT"
    ORG = "ORG"
    def list():
        return list(map(lambda x: x.value, CreateTokenRequestScope._member_map_.values()))
class CreateTokenRequest(BaseModel):
    def __init__(self, scope: List[CreateTokenRequestScope], name: str):
        """
Initialize CreateTokenRequest 
Parameters:
----------
    scope: list of CreateTokenRequestScope
    name: str
        """
        self.scope= scope
        self.name= name