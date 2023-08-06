from .base import BaseModel
class Role(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class UpdateOrgMemberRequest(BaseModel):
    def __init__(self, role: Role):
        """
Initialize UpdateOrgMemberRequest 
Parameters:
----------
    role: Role
        """
        self.role= role