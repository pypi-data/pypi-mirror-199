from .base import BaseModel

class OrgResponse(BaseModel):
    def __init__(self, isAllowedForBeta: bool, isDeleted: bool, slug: str, domain: str, website: str, description: str, name: str, updatedAt: str, createdAt: str, id: float):
        """
Initialize OrgResponse 
Parameters:
----------
    isAllowedForBeta: bool
    isDeleted: bool
    slug: str
    domain: str
    website: str
    description: str
    name: str
    updatedAt: str
    createdAt: str
    id: float
        """
        self.isAllowedForBeta= isAllowedForBeta
        self.isDeleted= isDeleted
        self.slug= slug
        self.domain= domain
        self.website= website
        self.description= description
        self.name= name
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id