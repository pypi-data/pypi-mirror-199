from .base import BaseModel

class UserResponse(BaseModel):
    def __init__(self, isEnabled: bool, isLiblabAdmin: bool, lastName: str, firstName: str, email: str, updatedAt: str, createdAt: str, id: float):
        """
Initialize UserResponse 
Parameters:
----------
    isEnabled: bool
    isLiblabAdmin: bool
    lastName: str
    firstName: str
    email: str
    updatedAt: str
    createdAt: str
    id: float
        """
        self.isEnabled= isEnabled
        self.isLiblabAdmin= isLiblabAdmin
        self.lastName= lastName
        self.firstName= firstName
        self.email= email
        self.updatedAt= updatedAt
        self.createdAt= createdAt
        self.id= id