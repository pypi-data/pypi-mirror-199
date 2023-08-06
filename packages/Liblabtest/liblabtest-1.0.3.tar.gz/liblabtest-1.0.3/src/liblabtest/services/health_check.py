from urllib.parse import quote
from .base import BaseService
from ..models.HealthCheckResponse import HealthCheckResponse as HealthCheckResponseModel
class HealthCheck(BaseService):
  def health_check_controller_check(self) -> HealthCheckResponseModel:

    url_endpoint = '/health-check'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.get(final_url, headers, True)
    if res and isinstance(res, dict):
        return HealthCheckResponseModel(**res)
    else:
        return res






