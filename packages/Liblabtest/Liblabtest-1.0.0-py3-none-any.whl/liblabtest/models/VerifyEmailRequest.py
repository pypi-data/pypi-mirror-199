from .base import BaseModel

class VerifyEmailRequest(BaseModel):
    def __init__(self, code: str, email: str):
        """
Initialize VerifyEmailRequest 
Parameters:
----------
    code: str
    email: str
        """
        self.code= code
        self.email= email