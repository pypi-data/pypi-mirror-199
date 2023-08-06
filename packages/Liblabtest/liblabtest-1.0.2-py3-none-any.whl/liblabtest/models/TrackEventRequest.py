from .base import BaseModel
class Metadata(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class TrackEventRequest(BaseModel):
    def __init__(self, name: str, metadata: Metadata=None, userToken: str=None):
        """
Initialize TrackEventRequest 
Parameters:
----------
    name: str
    metadata: Metadata
    userToken: str
        """
        self.name= name
        if metadata is not None:
            self.metadata= metadata
        if userToken is not None:
            self.userToken= userToken