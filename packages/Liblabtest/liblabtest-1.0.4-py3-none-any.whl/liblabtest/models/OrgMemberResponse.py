from .base import BaseModel
from enum import Enum
class Role(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    def list():
        return list(map(lambda x: x.value, Role._member_map_.values()))
class OrgMemberResponse(BaseModel):
    def __init__(self, isEnabled: bool, role: Role, userId: float, orgId: float, updatedAt: str, createdAt: str):
        """
Initialize OrgMemberResponse 
Parameters:
----------
    isEnabled: bool
    role: str
    userId: float
    orgId: float
    updatedAt: str
    createdAt: str
        """
        self.isEnabled= isEnabled
        self.role = self._enum_matching(role, Role.list(), "role")
        self.userId= userId
        self.orgId= orgId
        self.updatedAt= updatedAt
        self.createdAt= createdAt