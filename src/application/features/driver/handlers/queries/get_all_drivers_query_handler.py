from dataclasses import dataclass

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.application.features.common.dtos import DriverDto
from src.application.features.common.dtos.business_dto import LocationDto
from src.application.features.common.dtos.car_dto import CarDto
from src.application.features.driver.requests.queries.get_all_drivers_query import \
    GetAllDriversQuery


@request_handler(GetAllDriversQuery, BaseResponse[list[DriverDto]])
@dataclass
class GetAllDriversQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetAllDriversQuery) -> BaseResponse[list[DriverDto]]:
        if drivers := self._uow.driver_repository.get_all():
            return BaseResponse[list[DriverDto]].success(
                "Drivers fetched successfully.",
                [
                    DriverDto(
                        first_name=driver["first_name"],
                        last_name=driver["last_name"],
                        profile_image=driver["profile_image"],
                        phone_number=driver["phone_number"],
                        email=driver.get("email", ""),
                        car=CarDto(**self._uow.car_repository.get(id=driver["car_id"])), # type: ignore
                        location=LocationDto(**self._uow.location_repository.get(id=driver["location_id"])),# type: ignore
                    ) for driver in drivers
                ]
            )

        return BaseResponse[list[DriverDto]].error("Drivers couldn't be fetched.", ["There are no drivers."])
