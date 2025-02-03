from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.common.dtos import DeliveryJobDto, LocationDto
from src.application.features.driver.requests.queries import GetDeliveryJobsQuery


@request_handler(GetDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        if business := self._uow.business_repository.get(id=request.business_id):
            return BaseResponse[list[DeliveryJobDto]].success(
                "DeliveryJob fetched successfully.",
                DeliveryJobDto(
                    **business,
                    location=LocationDto(
                        **self._uow.location_repository.get(id=business["location_id"]),  # type: ignore
                    ),
                ),
            )

        return BaseResponse[list[DeliveryJobDto]].error(
            "DeliveryJob not found.",
            [f"Buisness with id {request.business_id} not found."],
        )
