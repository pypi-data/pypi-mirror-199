from urllib.parse import quote
from .base import BaseService
from ..models.OrgGetByCurrentUser200Response import OrgGetByCurrentUser200Response as OrgGetByCurrentUser200ResponseModel
from ..models.OrgCreateRequest import OrgCreateRequest as OrgCreateRequestModel
from ..models.OrgResponse import OrgResponse as OrgResponseModel
from ..models.OrgUpdateRequest import OrgUpdateRequest as OrgUpdateRequestModel
from ..models.OrgGetApis200Response import OrgGetApis200Response as OrgGetApis200ResponseModel
from ..models.OrgGetPayments200Response import OrgGetPayments200Response as OrgGetPayments200ResponseModel
from ..models.OrgGetArtifacts200Response import OrgGetArtifacts200Response as OrgGetArtifacts200ResponseModel
from ..models.OrgGetDocs200Response import OrgGetDocs200Response as OrgGetDocs200ResponseModel
class Org(BaseService):
  def get_by_current_user(self) -> OrgGetByCurrentUser200ResponseModel:

    url_endpoint = '/orgs'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return OrgGetByCurrentUser200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: OrgCreateRequestModel) -> OrgResponseModel:

    url_endpoint = '/orgs'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return OrgResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> OrgResponseModel:

    url_endpoint = '/orgs/{id}'
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
        return OrgResponseModel(**res)
    else:
        return res


  def update(self, request_input: OrgUpdateRequestModel, id:float) -> OrgResponseModel:

    url_endpoint = '/orgs/{id}'
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
        return OrgResponseModel(**res)
    else:
        return res
  def remove(self, id:float):

    url_endpoint = '/orgs/{id}'
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



  def get_apis(self, id:float) -> OrgGetApis200ResponseModel:

    url_endpoint = '/orgs/{id}/apis'
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
        return OrgGetApis200ResponseModel(**res)
    else:
        return res







  def get_payments(self, id:float) -> OrgGetPayments200ResponseModel:

    url_endpoint = '/orgs/{id}/payments'
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
        return OrgGetPayments200ResponseModel(**res)
    else:
        return res







  def get_artifacts(self, id:float) -> OrgGetArtifacts200ResponseModel:

    url_endpoint = '/orgs/{id}/artifacts'
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
        return OrgGetArtifacts200ResponseModel(**res)
    else:
        return res







  def get_docs(self, id:float) -> OrgGetDocs200ResponseModel:

    url_endpoint = '/orgs/{id}/docs'
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
        return OrgGetDocs200ResponseModel(**res)
    else:
        return res






