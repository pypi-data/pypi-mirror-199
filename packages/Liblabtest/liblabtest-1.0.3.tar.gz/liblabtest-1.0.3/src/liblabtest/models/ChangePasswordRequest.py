from .base import BaseModel

class ChangePasswordRequest(BaseModel):
    def __init__(self, password: str):
        """
Initialize ChangePasswordRequest 
Parameters:
----------
    password: str
        """
        self.password= password