from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos import BusinessDto
from src.application.features.business.requests.queries import GetBusinessQuery
from src.application.features.driver.dtos.driver_dto import LocationDto


@request_handler(GetBusinessQuery, BaseResponse[BusinessDto])
class GetBusinessByUserIdQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetBusinessQuery) -> BaseResponse[BusinessDto]:
        if business := self._uow.business_repository.get(user_id=request.user_id):
            return BaseResponse[BusinessDto].success(
                "Business fetched successfully.",
                BusinessDto(
                    **business,
                    location=LocationDto(
                        **self._uow.location_repository.get(id=business["location_id"]),  # type: ignore
                    ),
                ),
            )

        return BaseResponse[BusinessDto].error(
            "Business not found.",
            [f"Buisness with id {request.business_id} not found."],
        )
