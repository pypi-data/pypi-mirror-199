from http_exceptions import client_exceptions
from ..models.AuthTokenResponse import AuthTokenResponse
from ..models.AuthRefreshTokenRequest import AuthRefreshTokenRequest
from .http_client import HTTPClient


class HTTPWithAuthToken(HTTPClient):

    def __init__(self, http_client: HTTPClient, url_prefix: str, refresh_token: str = '', bearer_token: str = ''):
        self._http = http_client
        self._url_prefix = url_prefix
        self._refresh_token = refresh_token
        self._bearer_token = bearer_token

    def set_url(self, url: str):
        self._url_prefix = url

    def set_refresh_token(self, refresh_token):
        self._refresh_token = refresh_token

    def set_bearer_token(self, bearer_token):
        self._bearer_token = bearer_token

    def _with_refresh_token(self, callback_fn):
        if not self._bearer_token and self._refresh_token:
            self.refresh_bearer_token()

        try:
            result = callback_fn()
        except client_exceptions.UnauthorizedException as ex:
            if self._refresh_token:
                self.refresh_bearer_token()
                result = callback_fn()

        return result

    def refresh_bearer_token(self):
        url_endpoint = '/auth/refresh-jwt'
        final_url = self._url_prefix + url_endpoint
        response = self._http.post(final_url, self._get_required_headers(), AuthRefreshTokenRequest(self._refresh_token), True)

        response_model = AuthTokenResponse(**response)

        self.set_refresh_token(response_model.refreshToken)
        self.set_bearer_token(response_model.accessToken)

    def _get_required_headers(self):
        if not self._bearer_token:
            return {}
        headers = {
            'Authorization': f'Bearer {self._bearer_token}'
        }
        return headers

    def get(self, url: str, headers: dict, retry: bool = True):
        return self._with_refresh_token(lambda: self._http.get(url, {**self._get_required_headers(), **headers}, retry))

    def patch(self, url: str, headers: dict, body_input, retry: bool = True):
        return self._with_refresh_token(lambda: self._http.patch(url, {**self._get_required_headers(), **headers}, body_input, retry))

    def post(self, url: str, headers: dict, body_input, retry: bool = True):
        return self._with_refresh_token(lambda: self._http.post(url, {**self._get_required_headers(), **headers}, body_input, retry))

    def put(self, url: str, headers: dict, body_input, retry: bool = True):
        return self._with_refresh_token(lambda: self._http.put(url, {**self._get_required_headers(), **headers}, body_input, retry))

    def delete(self, url: str, headers: dict, retry: bool = True):
        return self._with_refresh_token(lambda: self._http.delete(url, {**self._get_required_headers(), **headers}, retry))
