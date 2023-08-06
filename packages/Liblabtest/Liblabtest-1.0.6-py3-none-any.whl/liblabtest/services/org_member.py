from urllib.parse import quote
from .base import BaseService
from ..models.OrgmemberGetByOrgId200Response import OrgmemberGetByOrgId200Response as OrgmemberGetByOrgId200ResponseModel
from ..models.OrgmemberCreateMemberRequest import OrgmemberCreateMemberRequest as OrgmemberCreateMemberRequestModel
from ..models.OrgMemberResponse import OrgMemberResponse as OrgMemberResponseModel
from ..models.OrgmemberUpdateMemberRequest import OrgmemberUpdateMemberRequest as OrgmemberUpdateMemberRequestModel
from ..models.UpdateManyOrgMembersResponse import UpdateManyOrgMembersResponse as UpdateManyOrgMembersResponseModel
class OrgMember(BaseService):
  def get_by_org_id(self, org_id:float) -> OrgmemberGetByOrgId200ResponseModel:

    url_endpoint = '/orgs/{org_id}/members'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return OrgmemberGetByOrgId200ResponseModel(**res)
    else:
        return res
  def create_member(self, request_input: OrgmemberCreateMemberRequestModel, org_id:float) -> OrgMemberResponseModel:

    url_endpoint = '/orgs/{org_id}/members'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return OrgMemberResponseModel(**res)
    else:
        return res









  def update_member(self, request_input: OrgmemberUpdateMemberRequestModel, org_id:float, member_id:float) -> OrgMemberResponseModel:

    url_endpoint = '/orgs/{org_id}/members/{member_id}'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not member_id:
        raise ValueError("Parameter member_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{member_id}', quote(str(member_id)))
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.patch(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return OrgMemberResponseModel(**res)
    else:
        return res
  def remove_member(self, org_id:float, member_id:float):

    url_endpoint = '/orgs/{org_id}/members/{member_id}'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not member_id:
        raise ValueError("Parameter member_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{member_id}', quote(str(member_id)))
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.delete(final_url, headers, True)
    return res






  def enable_all_members(self, org_id:float) -> UpdateManyOrgMembersResponseModel:

    url_endpoint = '/orgs/{org_id}/enable'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.patch(final_url, headers, {}, True)
    if res and isinstance(res, dict):
        return UpdateManyOrgMembersResponseModel(**res)
    else:
        return res







  def disable_all_members(self, org_id:float) -> UpdateManyOrgMembersResponseModel:

    url_endpoint = '/orgs/{org_id}/disable'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)
    if not org_id:
        raise ValueError("Parameter org_id is required, cannot be empty or blank.")
    url_endpoint = url_endpoint.replace('{org_id}', quote(str(org_id)))
    final_url = self._url_prefix + url_endpoint
    res = self._http.patch(final_url, headers, {}, True)
    if res and isinstance(res, dict):
        return UpdateManyOrgMembersResponseModel(**res)
    else:
        return res



