"""
Creates a Liblabtest class.
Generates the main SDK with all available queries as attributes.

Class:
    Liblabtest
"""
from .net.http_client import HTTPClient
from .net.http_with_auth_token import HTTPWithAuthToken
from .services.build import Build
from .services.api import Api
from .services.org import Org
from .services.artifact import Artifact
from .services.sdk import Sdk
from .services.doc import Doc
from .services.org_member import OrgMember
from .services.auth import Auth
from .services.user import User
from .services.token import Token
from .services.health_check import HealthCheck
from .services.event import Event



class Liblabtest:
    """
    A class representing the full Liblabtest SDK

    Attributes
    ----------
    build : Build
    api : Api
    org : Org
    artifact : Artifact
    sdk : Sdk
    doc : Doc
    org_member : OrgMember
    auth : Auth
    user : User
    token : Token
    health_check : HealthCheck
    event : Event

    Methods
    -------
    set_refresh_token(refresh_token)
        Set the refresh token
    set_bearer_token(bearer_token)
        Set the bearer token
    """
    
    
    def __init__(self, refresh_token = '', bearer_token = '') -> None:
        """
        Initializes the Liblabtest SDK class.

        Parameters
        ----------
        refresh_token : str
            The refresh token
        bearer_token : str
            The bearer token
        """
        self._http = HTTPWithAuthToken(HTTPClient(None), self._url_prefix, refresh_token, bearer_token)

        self.build= Build(self.http, self._url_prefix)
        self.api= Api(self.http, self._url_prefix)
        self.org= Org(self.http, self._url_prefix)
        self.artifact= Artifact(self.http, self._url_prefix)
        self.sdk= Sdk(self.http, self._url_prefix)
        self.doc= Doc(self.http, self._url_prefix)
        self.org_member= OrgMember(self.http, self._url_prefix)
        self.auth= Auth(self.http, self._url_prefix)
        self.user= User(self.http, self._url_prefix)
        self.token= Token(self.http, self._url_prefix)
        self.health_check= HealthCheck(self.http, self._url_prefix)
        self.event= Event(self.http, self._url_prefix)







