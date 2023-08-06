from urllib.parse import quote
from .base import BaseService
from ..models.GetTokenResponse import GetTokenResponse as GetTokenResponseModel
from ..models.TokenCreateRequest import TokenCreateRequest as TokenCreateRequestModel
from ..models.CreateTokenResponse import CreateTokenResponse as CreateTokenResponseModel
class Token(BaseService):
  def find_by_user_id(self, user_id:float) -> GetTokenResponseModel:

    url_endpoint = '/auth/tokens'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not user_id:
        raise ValueError("Parameter user_id is required, cannot be empty or blank.")
    if user_id:
        query_params.append(f"userId={user_id}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return GetTokenResponseModel(**res)
    else:
        return res
  def create(self, request_input: TokenCreateRequestModel) -> CreateTokenResponseModel:

    url_endpoint = '/auth/tokens'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return CreateTokenResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> GetTokenResponseModel:

    url_endpoint = '/auth/tokens/{id}'
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
        return GetTokenResponseModel(**res)
    else:
        return res



  def remove(self, id:float):

    url_endpoint = '/auth/tokens/{id}'
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


