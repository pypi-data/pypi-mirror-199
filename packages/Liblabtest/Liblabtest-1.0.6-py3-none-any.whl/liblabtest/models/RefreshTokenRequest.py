from .base import BaseModel

class RefreshTokenRequest(BaseModel):
    def __init__(self, refreshToken: str):
        """
Initialize RefreshTokenRequest 
Parameters:
----------
    refreshToken: str
        """
        self.refreshToken= refreshToken