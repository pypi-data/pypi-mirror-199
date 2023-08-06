"""
Creates a BaseService class.
Performs API calls,sets authentication tokens and handles http exceptions.

Class:
    BaseService
"""
from time import sleep
from typing import List
import requests
import re
from http_exceptions import HTTPException, client_exceptions, server_exceptions
from ..net.http_client import HTTPClient


class BaseService:
    """
    A class to represent a base serivce

    Attributes
    ----------
    _url_prefix : str
        The base URL

    Methods
    -------
    def _add_required_headers(headers: dict):
        Request authorization headers
    """



    def __init__(self, http: HTTPClient, url_prefix: str) -> None:
        """
        Initialize client
        
        Parameters:
        ----------
            http : HTTPClient 
                The http client
            url_prefix:
                The base url
        """
        self._http = http
        self._url_prefix = url_prefix


    def _pattern_matching(cls, value: str, pattern: str, variable_name: str):
        if re.match(r'{}'.format(pattern), value):
            return value
        else:
            raise ValueError(f'Invalid value for {variable_name}: must match {pattern}')

    def _enum_matching(cls, value: str, enum_values: List[str], variable_name: str):
        if value in enum_values:
            return value
        else:
            raise ValueError(f'Invalid value for {variable_name}: must match one of {enum_values}')





    
    def _add_required_headers(self, headers: dict):
        """
        Request authorization headers
        
        Parameters
        ----------
        headers: dict
            Headers dict to add auth headers to
        """
        headers["User-Agent"] = "liblab/0.1.0 LiblabTestSDK/1.0 python/3.11.2"
        
        return headers
 

