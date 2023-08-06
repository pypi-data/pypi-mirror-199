from __future__ import annotations
from .base import BaseModel
from typing import List
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ArtifactResponse import ArtifactResponse
class BuildType(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class Status(Enum):
    SUCCESS = "SUCCESS"
    IN_PROGRESS = "IN_PROGRESS"
    FAILURE = "FAILURE"
    def list():
        return list(map(lambda x: x.value, Status._member_map_.values()))
class BuildResponse(BaseModel):
    def __init__(self, buildType: BuildType, apiId: float, endTime: str, startTime: str, status: Status, updatedAt: str, createdAt: str, id: float, artifacts: List[ArtifactResponse]=None):
        """
Initialize BuildResponse 
Parameters:
----------
    buildType: BuildType
    apiId: float
    endTime: str
    startTime: str
    status: str
    updatedAt: str
    createdAt: str
    id: float
    artifacts: list of ArtifactResponse
        """
        self.buildType= buildType
        self.apiId= apiId
        self.endTime= endTime
        self.startTime= startTime
        self.status = self._enum_matching(status, Status.list(), "status")
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id
        if artifacts is not None:
            self.artifacts= artifacts