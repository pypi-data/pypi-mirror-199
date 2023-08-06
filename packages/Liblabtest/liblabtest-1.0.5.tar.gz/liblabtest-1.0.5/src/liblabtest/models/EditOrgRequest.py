from .base import BaseModel

class EditOrgRequest(BaseModel):
    def __init__(self, name: str=None, description: str=None, website: str=None, domain: str=None):
        """
Initialize EditOrgRequest 
Parameters:
----------
    name: str
    description: str
    website: str
    domain: str
        """
        if name is not None:
            self.name= name
        if description is not None:
            self.description= description
        if website is not None:
            self.website= website
        if domain is not None:
            self.domain= domain