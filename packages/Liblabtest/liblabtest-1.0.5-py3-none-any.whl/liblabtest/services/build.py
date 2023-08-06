from urllib.parse import quote
from .base import BaseService
from ..models.BuildBuildSdkRequest import BuildBuildSdkRequest as BuildBuildSdkRequestModel
from ..models.BuildResponse import BuildResponse as BuildResponseModel
from ..models.BuildBuildDocRequest import BuildBuildDocRequest as BuildBuildDocRequestModel
from ..models.BuildGetBuilds200Response import BuildGetBuilds200Response as BuildGetBuilds200ResponseModel
class Build(BaseService):

  def build_sdk(self, request_input: BuildBuildSdkRequestModel) -> BuildResponseModel:

    url_endpoint = '/builds/sdk'
    headers = {'Content-type' : 'multipart/form-data'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return BuildResponseModel(**res)
    else:
        return res







  def build_doc(self, request_input: BuildBuildDocRequestModel) -> BuildResponseModel:

    url_endpoint = '/builds/doc'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return BuildResponseModel(**res)
    else:
        return res






  def get_builds(self, api_id:float) -> BuildGetBuilds200ResponseModel:

    url_endpoint = '/builds'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not api_id:
        raise ValueError("Parameter api_id is required, cannot be empty or blank.")
    if api_id:
        query_params.append(f"apiId={api_id}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return BuildGetBuilds200ResponseModel(**res)
    else:
        return res







  def get_by_id(self, id:float) -> BuildResponseModel:

    url_endpoint = '/builds/{id}'
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
        return BuildResponseModel(**res)
    else:
        return res






