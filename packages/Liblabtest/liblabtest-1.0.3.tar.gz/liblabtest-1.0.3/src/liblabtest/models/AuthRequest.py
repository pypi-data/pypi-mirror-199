from .base import BaseModel

class AuthRequest(BaseModel):
    def __init__(self, password: str, email: str):
        """
Initialize AuthRequest 
Parameters:
----------
    password: str
    email: str
        """
        self.password = self._pattern_matching(password, '^((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z])(?=.*\W+).*$', "password")
        self.email= email