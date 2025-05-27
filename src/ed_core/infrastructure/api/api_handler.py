from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_notification.documentation.api.abc_notification_api_client import \
    ABCNotificationApiClient

from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi


class ApiHandler(ABCApi):
    def __init__(
        self, auth_api: ABCAuthApiClient, notification_api: ABCNotificationApiClient
    ) -> None:
        self._auth_api = auth_api
        self._notification_api = notification_api

    @property
    def auth_api(self) -> ABCAuthApiClient:
        return self._auth_api

    @property
    def notification_api(self) -> ABCNotificationApiClient:
        return self._notification_api
