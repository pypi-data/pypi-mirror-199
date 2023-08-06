from .base import BaseModel
from typing import List
from enum import Enum
class CreateSdkBuildRequestLanguages(Enum):
    JAVA = "java"
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    BASH = "bash"
    SPEC = "spec"
    def list():
        return list(map(lambda x: x.value, CreateSdkBuildRequestLanguages._member_map_.values()))

class CreateSdkBuildRequestDeliveryMethods(Enum):
    FILES = "files"
    ZIP = "zip"
    TAR = "tar"
    GITHUB = "github"
    JSON = "json"
    NONE = "none"
    def list():
        return list(map(lambda x: x.value, CreateSdkBuildRequestDeliveryMethods._member_map_.values()))

class CreateSdkBuildRequestAuth(Enum):
    APIKEY = "apikey"
    BASIC = "basic"
    BEARER = "bearer"
    CUSTOM = "custom"
    def list():
        return list(map(lambda x: x.value, CreateSdkBuildRequestAuth._member_map_.values()))

class HttpClient(Enum):
    AXIOS = "axios"
    FETCH = "fetch"
    HTTPS = "https"
    def list():
        return list(map(lambda x: x.value, HttpClient._member_map_.values()))

class Plugins(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class Retry(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class HooksLocation(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class CustomQueriesLocation(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
class CreateSdkBuildRequest(BaseModel):
    def __init__(self, spec: str, apiVersion: str, apiName: str, languages: List[CreateSdkBuildRequestLanguages], deliveryMethods: List[CreateSdkBuildRequestDeliveryMethods], sdkVersion: str, sdkName: str, specUrl: str=None, baseUrl: str=None, auth: List[CreateSdkBuildRequestAuth]=None, httpClient: HttpClient=None, generateEnv: bool=None, multiTenant: bool=None, npmName: str=None, npmOrg: str=None, plugins: Plugins=None, retry: Retry=None, hooksLocation: HooksLocation=None, customQueriesLocation: CustomQueriesLocation=None, hooks: str=None, customQueries: str=None):
        """
Initialize CreateSdkBuildRequest 
Parameters:
----------
    spec: str
    apiVersion: str
    apiName: str
    languages: list of CreateSdkBuildRequestLanguages
    deliveryMethods: list of CreateSdkBuildRequestDeliveryMethods
    sdkVersion: str
    sdkName: str
    specUrl: str
    baseUrl: str
    auth: list of CreateSdkBuildRequestAuth
    httpClient: str
    generateEnv: bool
    multiTenant: bool
    npmName: str
    npmOrg: str
    plugins: Plugins
    retry: Retry
    hooksLocation: HooksLocation
    customQueriesLocation: CustomQueriesLocation
    hooks: str
    customQueries: str
        """
        self.spec= spec
        self.apiVersion = self._pattern_matching(apiVersion, '^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$', "apiVersion")
        self.apiName= apiName
        self.languages= languages
        self.deliveryMethods= deliveryMethods
        self.sdkVersion= sdkVersion
        self.sdkName= sdkName
        if specUrl is not None:
            self.specUrl= specUrl
        if baseUrl is not None:
            self.baseUrl= baseUrl
        if auth is not None:
            self.auth= auth
        if httpClient is not None:
            self.httpClient = self._enum_matching(httpClient, HttpClient.list(), "httpClient")
        if generateEnv is not None:
            self.generateEnv= generateEnv
        if multiTenant is not None:
            self.multiTenant= multiTenant
        if npmName is not None:
            self.npmName= npmName
        if npmOrg is not None:
            self.npmOrg= npmOrg
        if plugins is not None:
            self.plugins= plugins
        if retry is not None:
            self.retry= retry
        if hooksLocation is not None:
            self.hooksLocation= hooksLocation
        if customQueriesLocation is not None:
            self.customQueriesLocation= customQueriesLocation
        if hooks is not None:
            self.hooks= hooks
        if customQueries is not None:
            self.customQueries= customQueries