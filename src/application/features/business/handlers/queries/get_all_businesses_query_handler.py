from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos.business_dto import BusinessDto
from src.application.features.business.requests.queries import GetBusinessQuery
from src.application.features.driver.dtos.driver_dto import LocationDto


@request_handler(GetBusinessQuery, BaseResponse[list[BusinessDto]])
class GetAllBusinessesQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessQuery
    ) -> BaseResponse[list[BusinessDto]]:
        businesses = self._uow.business_repository.get_all()

        return BaseResponse[list[BusinessDto]].success(
            "Business fetched successfully.",
            [
                BusinessDto(
                    **business,
                    location=LocationDto(
                        **self._uow.location_repository.get(id=business["location_id"]),  # type: ignore
                    ),
                )
                for business in businesses
            ],
        )
