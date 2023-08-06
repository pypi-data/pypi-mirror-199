from urllib.parse import quote
from .base import BaseService
from ..models.SdkFindSdks200Response import SdkFindSdks200Response as SdkFindSdks200ResponseModel
from ..models.SdkCreateRequest import SdkCreateRequest as SdkCreateRequestModel
from ..models.SdkResponse import SdkResponse as SdkResponseModel
class Sdk(BaseService):
  def find_sdks(self, artifact_id:float, limit:float, offset:float) -> SdkFindSdks200ResponseModel:

    url_endpoint = '/sdks'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not offset:
        raise ValueError("Parameter offset is required, cannot be empty or blank.")
    if offset:
        query_params.append(f"offset={offset}")
    if not limit:
        raise ValueError("Parameter limit is required, cannot be empty or blank.")
    if limit:
        query_params.append(f"limit={limit}")
    if not artifact_id:
        raise ValueError("Parameter artifact_id is required, cannot be empty or blank.")
    if artifact_id:
        query_params.append(f"artifactId={artifact_id}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return SdkFindSdks200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: SdkCreateRequestModel) -> SdkResponseModel:

    url_endpoint = '/sdks'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return SdkResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> SdkResponseModel:

    url_endpoint = '/sdks/{id}'
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
        return SdkResponseModel(**res)
    else:
        return res



  def remove(self, id:float):

    url_endpoint = '/sdks/{id}'
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


