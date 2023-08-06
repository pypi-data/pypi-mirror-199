from urllib.parse import quote
from .base import BaseService
from ..models.DocFindDocs200Response import DocFindDocs200Response as DocFindDocs200ResponseModel
from ..models.DocCreateRequest import DocCreateRequest as DocCreateRequestModel
from ..models.DocCreatedResponse import DocCreatedResponse as DocCreatedResponseModel
from ..models.DocResponse import DocResponse as DocResponseModel
from ..models.DocUpdateRequest import DocUpdateRequest as DocUpdateRequestModel
class Doc(BaseService):
  def find_docs(self, artifact_id:float, limit:float, offset:float) -> DocFindDocs200ResponseModel:

    url_endpoint = '/docs'
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
        return DocFindDocs200ResponseModel(**res)
    else:
        return res
  def create(self, request_input: DocCreateRequestModel) -> DocCreatedResponseModel:

    url_endpoint = '/docs'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return DocCreatedResponseModel(**res)
    else:
        return res






  def get_approved_by_org_slug_and_api_slug(self, org_slug:str, api_slug:str=None, api_version:str=None) -> DocResponseModel:

    url_endpoint = '/docs/approved'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_slug:
        raise ValueError("Parameter org_slug is required, cannot be empty or blank.")
    if org_slug:
        query_params.append(f"orgSlug={org_slug}")
    if api_slug:
        query_params.append(f"apiSlug={api_slug}")
    if api_version:
        query_params.append(f"apiVersion={api_version}")
    final_url = self._url_prefix + url_endpoint + '?' + '&'.join(query_params)
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return DocResponseModel(**res)
    else:
        return res








  def approve(self, preview_slug:str) -> DocResponseModel:

    url_endpoint = '/docs/{preview_slug}/approve'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not preview_slug:
        raise ValueError("Parameter preview_slug is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{preview_slug}', quote(str(preview_slug)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, {}, True)
    if res and isinstance(res, dict):
        return DocResponseModel(**res)
    else:
        return res






  def get_by_id(self, id:float) -> DocResponseModel:

    url_endpoint = '/docs/{id}'
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
        return DocResponseModel(**res)
    else:
        return res

  def update(self, request_input: DocUpdateRequestModel, id:float) -> DocResponseModel:

    url_endpoint = '/docs/{id}'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not id:
        raise ValueError("Parameter id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{id}', quote(str(id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.put(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return DocResponseModel(**res)
    else:
        return res

  def remove(self, id:float) -> DocResponseModel:

    url_endpoint = '/docs/{id}'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not id:
        raise ValueError("Parameter id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{id}', quote(str(id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.delete(final_url, headers, True)
    if res and isinstance(res, dict):
        return DocResponseModel(**res)
    else:
        return res


