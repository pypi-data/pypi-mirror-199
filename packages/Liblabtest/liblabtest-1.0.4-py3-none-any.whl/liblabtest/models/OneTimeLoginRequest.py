from .base import BaseModel

class OneTimeLoginRequest(BaseModel):
    def __init__(self, code: str, email: str):
        """
Initialize OneTimeLoginRequest 
Parameters:
----------
    code: str
    email: str
        """
        self.code= code
        self.email= email