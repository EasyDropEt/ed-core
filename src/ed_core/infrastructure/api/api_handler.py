from ed_auth.documentation.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.auth_api_client import AuthApiClient

from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi


class ApiHandler(ABCApi):
    def __init__(self, auth_api: str) -> None:
        self._auth_api = AuthApiClient(auth_api)

    @property
    def auth_api(self) -> ABCAuthApiClient:
        return self._auth_api
