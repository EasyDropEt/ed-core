from abc import ABCMeta, abstractmethod

from ed_auth.documentation.abc_auth_api_client import ABCAuthApiClient


class ABCApi(metaclass=ABCMeta):
    @property
    @abstractmethod
    def auth_api(self) -> ABCAuthApiClient: ...
