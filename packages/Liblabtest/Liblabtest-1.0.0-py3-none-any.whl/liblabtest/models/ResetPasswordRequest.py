from .base import BaseModel

class ResetPasswordRequest(BaseModel):
    def __init__(self, email: str):
        """
Initialize ResetPasswordRequest 
Parameters:
----------
    email: str
        """
        self.email= email