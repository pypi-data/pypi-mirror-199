from .base import BaseModel

class CreateUserRequest(BaseModel):
    def __init__(self, password: str, email: str, firstName: str=None, lastName: str=None):
        """
Initialize CreateUserRequest 
Parameters:
----------
    password: str
    email: str
    firstName: str
    lastName: str
        """
        self.password= password
        self.email= email
        if firstName is not None:
            self.firstName= firstName
        if lastName is not None:
            self.lastName= lastName