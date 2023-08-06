from urllib.parse import quote
from .base import BaseService
from ..models.ArtifactGetArtifacts200Response import ArtifactGetArtifacts200Response as ArtifactGetArtifacts200ResponseModel
from ..models.ArtifactCreateRequest import ArtifactCreateRequest as ArtifactCreateRequestModel
from ..models.ArtifactResponse import ArtifactResponse as ArtifactResponseModel
from ..models.ApiResponse import ApiResponse as ApiResponseModel
class Artifact(BaseService):
  def get_artifacts(self, build_id:float) -> ArtifactGetArtifacts200ResponseModel:

    url_endpoint = '/artifacts'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not build_id:
        raise ValueError("Parameter build_id is required, cannot be empty or blank.")
    if build_id:
        query_params.append(f"buildId={build_id}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return ArtifactGetArtifacts200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: ArtifactCreateRequestModel) -> ArtifactResponseModel:

    url_endpoint = '/artifacts'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return ArtifactResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> ApiResponseModel:

    url_endpoint = '/artifacts/{id}'
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
        return ApiResponseModel(**res)
    else:
        return res



  def remove(self, id:float):

    url_endpoint = '/artifacts/{id}'
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


