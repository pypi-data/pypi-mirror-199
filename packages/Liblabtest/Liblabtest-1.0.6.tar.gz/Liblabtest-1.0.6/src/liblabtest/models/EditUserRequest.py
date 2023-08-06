from .base import BaseModel

class EditUserRequest(BaseModel):
    def __init__(self, email: str=None, firstName: str=None, lastName: str=None, refreshTokenHash: str=None, isLiblabAdmin: bool=None, isEnabled: bool=None):
        """
Initialize EditUserRequest 
Parameters:
----------
    email: str
    firstName: str
    lastName: str
    refreshTokenHash: str
    isLiblabAdmin: bool
    isEnabled: bool
        """
        if email is not None:
            self.email= email
        if firstName is not None:
            self.firstName= firstName
        if lastName is not None:
            self.lastName= lastName
        if refreshTokenHash is not None:
            self.refreshTokenHash= refreshTokenHash
        if isLiblabAdmin is not None:
            self.isLiblabAdmin= isLiblabAdmin
        if isEnabled is not None:
            self.isEnabled= isEnabled