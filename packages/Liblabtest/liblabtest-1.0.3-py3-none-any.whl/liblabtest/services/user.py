from urllib.parse import quote
from .base import BaseService
from ..models.UserResponse import UserResponse as UserResponseModel
from ..models.UserGetUserApis200Response import UserGetUserApis200Response as UserGetUserApis200ResponseModel
from ..models.UserCreateRequest import UserCreateRequest as UserCreateRequestModel
from ..models.UserUpdateRequest import UserUpdateRequest as UserUpdateRequestModel
class User(BaseService):
  def get_current_user(self) -> UserResponseModel:

    url_endpoint = '/users/current-user'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return UserResponseModel(**res)
    else:
        return res







  def get_user_apis(self) -> UserGetUserApis200ResponseModel:

    url_endpoint = '/users'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return UserGetUserApis200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: UserCreateRequestModel) -> UserResponseModel:

    url_endpoint = '/users'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return UserResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> UserResponseModel:

    url_endpoint = '/users/{id}'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not id:
        raise ValueError("Parameter id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{id}', quote(str(id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return UserResponseModel(**res)
    else:
        return res


  def update(self, request_input: UserUpdateRequestModel, id:float) -> UserResponseModel:

    url_endpoint = '/users/{id}'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not id:
        raise ValueError("Parameter id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{id}', quote(str(id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.patch(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return UserResponseModel(**res)
    else:
        return res
  def remove(self, id:float):

    url_endpoint = '/users/{id}'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not id:
        raise ValueError("Parameter id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{id}', quote(str(id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.delete(final_url, headers, True)
    return res


