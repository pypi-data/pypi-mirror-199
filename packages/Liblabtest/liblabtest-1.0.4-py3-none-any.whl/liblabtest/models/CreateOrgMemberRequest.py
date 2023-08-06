from .base import BaseModel
class Role(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class CreateOrgMemberRequest(BaseModel):
    def __init__(self, role: Role, userId: float):
        """
Initialize CreateOrgMemberRequest 
Parameters:
----------
    role: Role
    userId: float
        """
        self.role= role
        self.userId= userId