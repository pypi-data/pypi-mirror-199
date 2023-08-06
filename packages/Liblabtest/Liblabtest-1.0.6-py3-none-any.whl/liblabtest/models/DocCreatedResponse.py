from .base import BaseModel
from enum import Enum
class Status(Enum):
    ACCEPTED = "accepted"
    def list():
        return list(map(lambda x: x.value, Status._member_map_.values()))
class DocCreatedResponse(BaseModel):
    def __init__(self, buildId: float, status: Status):
        """
Initialize DocCreatedResponse 
Parameters:
----------
    buildId: float
    status: str
        """
        self.buildId= buildId
        self.status = self._enum_matching(status, Status.list(), "status")