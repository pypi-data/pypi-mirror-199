from .base import BaseModel

class ApiResponse(BaseModel):
    def __init__(self, specId: float, approvedDocId: float, orgId: float, version: str, slug: str, name: str, updatedAt: str, createdAt: str, id: float):
        """
Initialize ApiResponse 
Parameters:
----------
    specId: float
    approvedDocId: float
    orgId: float
    version: str
    slug: str
    name: str
    updatedAt: str
    createdAt: str
    id: float
        """
        self.specId= specId
        self.approvedDocId= approvedDocId
        self.orgId= orgId
        self.version= version
        self.slug= slug
        self.name= name
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id