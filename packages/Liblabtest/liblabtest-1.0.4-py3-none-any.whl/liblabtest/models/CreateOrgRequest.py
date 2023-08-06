from .base import BaseModel

class CreateOrgRequest(BaseModel):
    def __init__(self, name: str, description: str=None, website: str=None, domain: str=None):
        """
Initialize CreateOrgRequest 
Parameters:
----------
    name: str
    description: str
    website: str
    domain: str
        """
        self.name= name
        if description is not None:
            self.description= description
        if website is not None:
            self.website= website
        if domain is not None:
            self.domain= domain