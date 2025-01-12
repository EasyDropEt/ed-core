from datetime import UTC, datetime

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence import ABCUnitOfWork
from src.application.features.driver.dtos import CreateDriverDto, DriverDto
from src.application.features.driver.dtos.driver_dto import CarDto, LocationDto
from src.application.features.driver.dtos.validators import CreateDriverDtoValidator
from src.application.features.driver.requests.commands import CreateDriverCommand
from src.common.generic_helpers import get_new_id
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverCommand, BaseResponse[DriverDto])
class CreateDriverCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateDriverCommand) -> BaseResponse[DriverDto]:
        dto_validator = CreateDriverDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[DriverDto].error(
                "Create driver failed.", dto_validator.errors
            )

        dto: CreateDriverDto = request.dto

        car = self._uow.car_repository.create(
            {
                "id": get_new_id(),
                "driver_id": get_new_id(),
                "make": dto["car"]["make"],
                "model": dto["car"]["model"],
                "year": dto["car"]["year"],
                "registration_number": dto["car"]["registration_number"],
                "license_plate_number": dto["car"]["license_plate"],
                "color": dto["car"]["color"],
                "capacity": dto["car"]["seats"],
            }
        )

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

        driver = self._uow.driver_repository.create(
            {
                "id": get_new_id(),
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "profile_picture": dto["profile_image"],
                "phone_number": dto["phone_number"],
                "email": dto.get("email", ""),
                "location_id": location["id"],
                "car_id": car["id"],
                "delivery_job_ids": [],
                "payment_ids": [],
                #
                "user_id": dto["user_id"],
                "notification_ids": [],
                "active_status": True,
                "created_datetime": datetime.now(UTC),
                "updated_datetime": datetime.now(UTC),
            }
        )

        return BaseResponse[DriverDto].success(
            "Driver created successfully.",
            DriverDto(
                **driver,
                car=CarDto(**car),  # type: ignore
                location=LocationDto(**location),  # type: ignore
            ),
        )
