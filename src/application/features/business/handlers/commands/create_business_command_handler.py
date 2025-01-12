from datetime import UTC, datetime

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence import ABCUnitOfWork
from src.application.features.business.dtos import BusinessDto, CreateBusinessDto
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

        location = self._uow.location_repository.create(
            {
                "id": get_new_id(),
                "latitude": dto["location"]["latitude"],
                "longitude": dto["location"]["longitude"],
                "address": dto["location"]["address"],
                "city": dto["location"]["city"],
                "postal_code": dto["location"]["postal_code"],
                "country": "Ethiopia",
            }
        )

        business = self._uow.business_repository.create(
            {
                "id": get_new_id(),
                "business_name": dto["business_name"],
                "owner_first_name": dto["owner_first_name"],
                "owner_last_name": dto["owner_last_name"],
                "phone_number": dto["phone_number"],
                "email": dto.get("email", ""),
                "location_id": location["id"],
                "billing_details": dto["billing_details"],
                #
                "user_id": dto["user_id"],
                "notification_ids": [],
                "active_status": True,
                "created_datetime": datetime.now(UTC),
                "updated_datetime": datetime.now(UTC),
            }
        )

        return BaseResponse[BusinessDto].success(
            "Business created successfully.",
            BusinessDto(
                **business,
                location=LocationDto(**location),  # type: ignore
            ),
        )
