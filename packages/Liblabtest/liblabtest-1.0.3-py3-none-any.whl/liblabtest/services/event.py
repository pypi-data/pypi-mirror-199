from urllib.parse import quote
from .base import BaseService
from ..models.EventTrackRequest import EventTrackRequest as EventTrackRequestModel
class Event(BaseService):

  def track(self, request_input: EventTrackRequestModel):

    url_endpoint = '/events'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    return res





