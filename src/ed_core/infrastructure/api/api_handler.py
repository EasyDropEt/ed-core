from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.api.auth_api_client import AuthApiClient
from ed_notification.documentation.api.abc_notification_api_client import \
    ABCNotificationApiClient
from ed_notification.documentation.api.notification_api_client import \
    NotificationApiClient

from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.common.typing.config import Config


class ApiHandler(ABCApi):
    def __init__(self, config: Config) -> None:
        self._auth_api = AuthApiClient(config["auth_api"])
        self._notification_api = NotificationApiClient(
            config["notification_api"])

    @property
    def auth_api(self) -> ABCAuthApiClient:
        return self._auth_api

    @property
    def notification_api(self) -> ABCNotificationApiClient:
        return self._notification_api
