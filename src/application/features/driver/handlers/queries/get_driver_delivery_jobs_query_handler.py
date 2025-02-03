from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos.order_dto import OrderDto
from src.application.features.common.dtos import DeliveryJobDto
from src.application.features.common.dtos.route_dto import RouteDto
from src.application.features.driver.requests.queries.get_driver_delivery_jobs_query import (
    GetDriverDeliveryJobsQuery,
)


@request_handler(GetDriverDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDriverDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDriverDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        if delivery_jobs := self._uow.delivery_job_repository.get_all(
            driver_id=request.driver_id
        ):
            return BaseResponse[list[DeliveryJobDto]].success(
                "DeliveryJob fetched successfully.",
                [
                    DeliveryJobDto(
                        **delivery_job,
                        orders=[
                            OrderDto(
                                self._uow.order_repository.get(id=order_id),  # type: ignore
                            )
                            for order_id in delivery_job["order_ids"]
                        ],
                        route=RouteDto(
                            self._uow.route_repository.get(id=delivery_job["route_id"]),  # type: ignore
                        ),
                    )
                    for delivery_job in delivery_jobs
                ],
            )

        return BaseResponse[list[DeliveryJobDto]].error(
            "DeliveryJob not found.",
            [f"Delivery jobs for driver with id {request.business_id} not found."],
        )
