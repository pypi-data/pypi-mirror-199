from .base import BaseModel

class HealthCheckResponse(BaseModel):
    def __init__(self, status: str):
        """
Initialize HealthCheckResponse 
Parameters:
----------
    status: str
        """
        self.status= status