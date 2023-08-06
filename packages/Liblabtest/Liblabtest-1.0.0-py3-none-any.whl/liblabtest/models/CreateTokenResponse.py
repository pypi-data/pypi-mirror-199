from .base import BaseModel

class CreateTokenResponse(BaseModel):
    def __init__(self, expiresAt: str, token: str, name: str, id: float):
        """
Initialize CreateTokenResponse 
Parameters:
----------
    expiresAt: str
        Defaults to 1 year from creation date
    token: str
        Warning: only shown once, please save securely
    name: str
    id: float
        """
        self.expiresAt= expiresAt
        self.token= token
        self.name= name
        self.id= id