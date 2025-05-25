from fastapi.middleware.cors import CORSMiddleware

from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._api = API(
            title="ED Core Service",
            description="Core Service API Documentation",
        )
        self._api.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def start(self) -> None:
        self._api.start()

    def stop(self) -> None:
        self._api.stop()


if __name__ == "__main__":
    main = Package()

    main.start()
