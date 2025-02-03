from datetime import UTC, datetime

from ed_domain_model.entities import DeliveryJob, Route
from ed_domain_model.entities.delivery_job import DeliveryJobStatus
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.common.dtos import DeliveryJobDto
from src.application.features.common.dtos.route_dto import RouteDto
from src.application.features.delivery_job.dtos.create_delivery_job_dto import (
    CreateDeliveryJobDto,
)
from src.application.features.delivery_job.requests.commands.create_delivery_job_command import (
    CreateDeliveryJobCommand,
)
from src.common.generic_helpers import get_new_id


@request_handler(CreateDeliveryJobCommand, BaseResponse[list[DeliveryJobDto]])
class CreateDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: CreateDeliveryJobCommand
    ) -> BaseResponse[list[DeliveryJobDto]]:
        dto: CreateDeliveryJobDto = request.dto
        route = self._uow.route_repository.create(
            Route(
                id=get_new_id(),
                waypoints=dto["route"]["waypoints"],
                estimated_distance_in_kms=dto["route"]["estimated_distance_in_kms"],
                estimated_time_in_minutes=dto["route"]["estimated_time_in_minutes"],
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
            )
        )

        delivery_job = self._uow.delivery_job_repository.create(
            DeliveryJob(
                id=get_new_id(),
                order_ids=dto["order_ids"],
                route_id=route["id"],
                status=DeliveryJobStatus.IN_PROGRESS,
                estimated_payment=dto["estimated_payment"],
                estimated_completion_time=dto["estimated_completion_time"],
            )
        )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery jobs created successfully.",
            DeliveryJobDto(
                **delivery_job,  # type: ignore
                orders=delivery_job["order_ids"],
                route=RouteDto(**route),  # type: ignore
            ),
        )
