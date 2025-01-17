from datetime import UTC, datetime

from ed_domain_model.entities import Business, Location
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence import ABCUnitOfWork
from src.application.features.business.dtos import (
    BusinessDto,
    CreateBusinessDto,
    CreateLocationDto,
)
from src.application.features.business.dtos.business_dto import LocationDto
from src.application.features.business.dtos.validators import CreateBusinessDtoValidator
from src.application.features.business.requests.commands import CreateBusinessCommand
from src.common.generic_helpers import get_new_id
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateBusinessCommand, BaseResponse[BusinessDto])
class CreateBusinessCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateBusinessCommand) -> BaseResponse[BusinessDto]:
        dto_validator = CreateBusinessDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[BusinessDto].error(
                "Create business failed.", dto_validator.errors
            )

        dto: CreateBusinessDto = request.dto

        location = await self._create_location(dto["location"])

        business = self._uow.business_repository.create(
            Business(
                **dto,  # type: ignore
                id=get_new_id(),
                location_id=location["id"],
                user_id=dto["user_id"],
                notification_ids=[],
                active_status=True,
                created_datetime=datetime.now(UTC),
                updated_datetime=datetime.now(UTC),
            )
        )

        return BaseResponse[BusinessDto].success(
            "Business created successfully.",
            BusinessDto(
                **business,
                location=LocationDto(**location),  # type: ignore
            ),
        )

    async def _create_location(self, location: CreateLocationDto) -> Location:
        return self._uow.location_repository.create(
            Location(
                **location,
                id=get_new_id(),
                city="Addis Ababa",
                country="Ethiopia",
            )
        )
