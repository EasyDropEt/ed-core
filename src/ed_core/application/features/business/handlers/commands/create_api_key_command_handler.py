import secrets
import uuid

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.application.features.business.requests.commands import \
    CreateApiKeyCommand
from ed_core.application.features.common.dtos import ApiKeyDto

LOG = get_logger()

BILL_AMOUNT = 10


@request_handler(CreateApiKeyCommand, BaseResponse[ApiKeyDto])
class CreateApiKeyCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        password: ABCPasswordHandler,
    ):
        self._uow = uow
        self._password = password

        self._error_message = "Failed to created API key."
        self._success_message = "API key created succesfully."

    async def handle(self, request: CreateApiKeyCommand) -> BaseResponse[ApiKeyDto]:
        prefix, key = self._generate_api_key()
        key_hash = self._password.hash(key)

        async with self._uow.transaction():
            api_key = await request.dto.create_api_key(
                request.business_id, prefix, key_hash, self._uow
            )

        if api_key is None:
            raise ApplicationException(
                Exceptions.InternalServerException,
                self._error_message,
                ["Internal server exception."],
            )

        return BaseResponse[ApiKeyDto].success(
            self._success_message,
            ApiKeyDto(**api_key.__dict__),
        )

    def _generate_api_key(self, key_length: int = 48) -> tuple[str, str]:
        prefix = str(uuid.uuid4())[:8].replace("-", "")
        random_key_part = secrets.token_urlsafe(key_length)

        plaintext_key = f"{prefix}_{random_key_part}"

        return prefix, plaintext_key
