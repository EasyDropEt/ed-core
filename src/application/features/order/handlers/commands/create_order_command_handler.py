from datetime import UTC, datetime
from uuid import UUID

from ed_domain_model.entities import Bill, Consumer, Order
from ed_domain_model.entities.order import OrderStatus
from ed_domain_model.queues.order.order_model import (
    BusinessModel,
    ConsumerModel,
    OrderModel,
)
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.message_queue.abc_producer import (
    ABCProducer,
)
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
    def __init__(self, uow: ABCUnitOfWork, producer: ABCProducer[OrderModel]):
        self._uow = uow
        self._producer = producer

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]:
        business_id = request.business_id
        dto: CreateOrderDto = request.dto
        dto_validator = CreateOrderDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[OrderDto].error(
                "Order cannot be created.",
                dto_validator.errors,
            )

        consumer = await self._create_or_get_consumer(dto["consumer"])
        bill = await self._create_bill(business_id)
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

        await self._publish_order(created_order, consumer)

        return BaseResponse[OrderDto].success(
            "Order created successfully.",
            OrderDto(
                **created_order,
                consumer=ConsumerDto(**consumer),  # type: ignore
            ),
        )

    async def _publish_order(self, order: Order, consumer: Consumer) -> None:
        return self._producer.publish(
            {
                "id": order["id"],
                "consumer": ConsumerModel(**consumer),  # type: ignore
                "business": BusinessModel(
                    **self._uow.business_repository.get(id=order["business_id"])  # type: ignore
                ),
                "bill_id": order["bill_id"],
                "latest_time_of_delivery": order["latest_time_of_delivery"],
                "parcel": order["parcel"],
                "order_status": OrderStatus.PENDING,
            }
        )

    async def _create_bill(self, business_id: UUID) -> Bill:
        return self._uow.bill_repository.create(
            {
                "id": get_new_id(),
                "business_id": business_id,
                "amount": 10.0,
            }
        )

    async def _create_or_get_consumer(self, dto: ConsumerDto) -> Consumer:
        return self._uow.consumer_repository.get(
            phone_number=dto["phone_number"]
        ) or self._uow.consumer_repository.create(
            {
                "id": get_new_id(),
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "phone_number": dto["phone_number"],
                "email": dto.get("email", ""),
                "user_id": get_new_id(),
                "active_status": True,
                "created_datetime": datetime.now(UTC),
                "updated_datetime": datetime.now(UTC),
                "notification_ids": [],
            }
        )
