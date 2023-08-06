from .base import BaseModel

class AuthTokenResponse(BaseModel):
    def __init__(self, refreshToken: str, accessToken: str):
        """
Initialize AuthTokenResponse 
Parameters:
----------
    refreshToken: str
    accessToken: str
        """
        self.refreshToken= refreshToken
        self.accessToken= accessToken