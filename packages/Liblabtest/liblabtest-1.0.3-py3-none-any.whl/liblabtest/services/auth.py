from urllib.parse import quote
from .base import BaseService
from ..models.AuthSignupRequest import AuthSignupRequest as AuthSignupRequestModel
from ..models.AuthLoginRequest import AuthLoginRequest as AuthLoginRequestModel
from ..models.AuthTokenResponse import AuthTokenResponse as AuthTokenResponseModel
from ..models.AuthRefreshTokenRequest import AuthRefreshTokenRequest as AuthRefreshTokenRequestModel
from ..models.AuthResetPasswordRequest import AuthResetPasswordRequest as AuthResetPasswordRequestModel
from ..models.AuthOneTimeLoginRequest import AuthOneTimeLoginRequest as AuthOneTimeLoginRequestModel
from ..models.AuthChangePasswordRequest import AuthChangePasswordRequest as AuthChangePasswordRequestModel
from ..models.AuthVerifyEmailRequest import AuthVerifyEmailRequest as AuthVerifyEmailRequestModel
class Auth(BaseService):

  def signup(self, request_input: AuthSignupRequestModel):

    url_endpoint = '/auth/signup'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    return res







  def login(self, request_input: AuthLoginRequestModel) -> AuthTokenResponseModel:

    url_endpoint = '/auth/login'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return AuthTokenResponseModel(**res)
    else:
        return res







  def logout(self):

    url_endpoint = '/auth/logout'
    headers = {}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, {}, True)
    return res







  def refresh_token(self, request_input: AuthRefreshTokenRequestModel) -> AuthTokenResponseModel:

    url_endpoint = '/auth/refresh-jwt'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return AuthTokenResponseModel(**res)
    else:
        return res







  def reset_password(self, request_input: AuthResetPasswordRequestModel):

    url_endpoint = '/auth/reset-password'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    return res







  def one_time_login(self, request_input: AuthOneTimeLoginRequestModel) -> AuthTokenResponseModel:

    url_endpoint = '/auth/one-time-login'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return AuthTokenResponseModel(**res)
    else:
        return res







  def change_password(self, request_input: AuthChangePasswordRequestModel) -> AuthTokenResponseModel:

    url_endpoint = '/auth/change-password'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    if res and isinstance(res, dict):
        return AuthTokenResponseModel(**res)
    else:
        return res







  def verify_email(self, request_input: AuthVerifyEmailRequestModel):

    url_endpoint = '/auth/verify-email'
    headers = {'Content-type' : 'application/json'}
    cookies = []
    query_params = []
    self._add_required_headers(headers)

    final_url = self._url_prefix + url_endpoint
    res = self._http.post(final_url, headers, request_input, True)
    return res





