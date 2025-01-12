from datetime import UTC, datetime

from ed_domain_model.entities.order import OrderStatus
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.order.dtos import CreateOrderDto, OrderDto
from src.application.features.order.dtos.order_dto import ConsumerDto
from src.application.features.order.dtos.validators import CreateOrderDtoValidator
from src.application.features.order.requests.commands import CreateOrderCommand
from src.common.generic_helpers import get_new_id
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrderCommand, BaseResponse[OrderDto])
class CreateOrderCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]:
        business_id = request.business_id
        dto: CreateOrderDto = request.dto
        dto_validator = CreateOrderDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[OrderDto].error(
                "Order cannot be created.",
                dto_validator.errors,
            )

        consumer = self._uow.consumer_repository.get(
            phone_number=dto["consumer"]["phone_number"]
        ) or self._uow.consumer_repository.create(
            {
                "id": get_new_id(),
                "first_name": dto["consumer"]["first_name"],
                "last_name": dto["consumer"]["last_name"],
                "phone_number": dto["consumer"]["phone_number"],
                "email": dto["consumer"].get("email", ""),
                "user_id": get_new_id(),
                "active_status": True,
                "created_datetime": datetime.now(UTC),
                "updated_datetime": datetime.now(UTC),
                "notification_ids": [],
            }
        )

        bill = self._uow.bill_repository.create(
            {
                "id": get_new_id(),
                "business_id": business_id,
                "amount": 10.0,
            }
        )

        created_order = self._uow.order_repository.create(
            {
                "id": get_new_id(),
                "consumer_id": consumer["id"],
                "business_id": business_id,
                "bill_id": bill["id"],
                "latest_time_of_delivery": dto["latest_time_of_delivery"],
                "parcel": dto["parcel"],
                "order_status": OrderStatus.PENDING,
            }
        )

        return BaseResponse[OrderDto].success(
            "Order created successfully.",
            OrderDto(
                **created_order,
                consumer=ConsumerDto(**consumer),  # type: ignore
            ),
        )
