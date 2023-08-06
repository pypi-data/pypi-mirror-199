from urllib.parse import quote
from .base import BaseService
from ..models.ApiGetApis200Response import ApiGetApis200Response as ApiGetApis200ResponseModel
from ..models.ApiCreateRequest import ApiCreateRequest as ApiCreateRequestModel
from ..models.ApiResponse import ApiResponse as ApiResponseModel
from ..models.ApiUpdateRequest import ApiUpdateRequest as ApiUpdateRequestModel
from ..models.ApiGetApiMembers200Response import ApiGetApiMembers200Response as ApiGetApiMembers200ResponseModel
from ..models.ApiGetApiSdks200Response import ApiGetApiSdks200Response as ApiGetApiSdks200ResponseModel
from ..models.ApiGetApiDocs200Response import ApiGetApiDocs200Response as ApiGetApiDocs200ResponseModel
from ..models.ApiGetApiBuilds200Response import ApiGetApiBuilds200Response as ApiGetApiBuilds200ResponseModel
from ..models.ApiGetApiByOrgSlugAndApiSlug200Response import ApiGetApiByOrgSlugAndApiSlug200Response as ApiGetApiByOrgSlugAndApiSlug200ResponseModel
class Api(BaseService):
  def get_apis(self, org_id:float) -> ApiGetApis200ResponseModel:

    url_endpoint = '/apis'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    if org_id:
        query_params.append(f"orgId={org_id}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return ApiGetApis200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: ApiCreateRequestModel) -> ApiResponseModel:

    url_endpoint = '/apis'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return ApiResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> ApiResponseModel:

    url_endpoint = '/apis/{id}'
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


  def update(self, request_input: ApiUpdateRequestModel, id:float) -> ApiResponseModel:

    url_endpoint = '/apis/{id}'
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
        return ApiResponseModel(**res)
    else:
        return res
  def remove(self, id:float):

    url_endpoint = '/apis/{id}'
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



  def get_api_members(self, id:float) -> ApiGetApiMembers200ResponseModel:

    url_endpoint = '/apis/{id}/members'
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
        return ApiGetApiMembers200ResponseModel(**res)
    else:
        return res







  def get_api_sdks(self, id:float) -> ApiGetApiSdks200ResponseModel:

    url_endpoint = '/apis/{id}/sdks'
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
        return ApiGetApiSdks200ResponseModel(**res)
    else:
        return res







  def get_api_docs(self, id:float) -> ApiGetApiDocs200ResponseModel:

    url_endpoint = '/apis/{id}/docs'
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
        return ApiGetApiDocs200ResponseModel(**res)
    else:
        return res







  def get_api_builds(self, id:float) -> ApiGetApiBuilds200ResponseModel:

    url_endpoint = '/apis/{id}/builds'
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
        return ApiGetApiBuilds200ResponseModel(**res)
    else:
        return res







  def get_api_by_org_slug_and_api_slug(self, api_slug:str, org_slug:str) -> ApiGetApiByOrgSlugAndApiSlug200ResponseModel:

    url_endpoint = '/apis/{org_slug}/{api_slug}'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_slug:
        raise ValueError("Parameter org_slug is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_slug}', quote(str(org_slug)))
    if not api_slug:
        raise ValueError("Parameter api_slug is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{api_slug}', quote(str(api_slug)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return ApiGetApiByOrgSlugAndApiSlug200ResponseModel(**res)
    else:
        return res






