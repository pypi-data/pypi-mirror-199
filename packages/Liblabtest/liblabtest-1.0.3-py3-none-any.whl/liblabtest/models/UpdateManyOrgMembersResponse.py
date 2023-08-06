from .base import BaseModel

class UpdateManyOrgMembersResponse(BaseModel):
    def __init__(self, count: float):
        """
Initialize UpdateManyOrgMembersResponse 
Parameters:
----------
    count: float
        """
        self.count= count