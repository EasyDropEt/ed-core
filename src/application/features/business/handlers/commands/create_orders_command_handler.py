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
from src.application.features.business.dtos import CreateOrdersDto, OrderDto
from src.application.features.business.dtos.order_dto import ConsumerDto
from src.application.features.business.dtos.validators.create_orders_dto_validator import (
    CreateOrdersDtoValidator,
)
from src.application.features.business.requests.commands.create_orders_command import (
    CreateOrdersCommand,
)
from src.common.generic_helpers import get_new_id
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrdersCommand, BaseResponse[list[OrderDto]])
class CreateOrdersCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, producer: ABCProducer[OrderModel]):
        self._uow = uow
        self._producer = producer

    async def handle(
        self, request: CreateOrdersCommand
    ) -> BaseResponse[list[OrderDto]]:
        business_id = request.business_id
        dto: CreateOrdersDto = request.dto
        dto_validator = CreateOrdersDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[list[OrderDto]].error(
                "Orders cannot be created.",
                dto_validator.errors,
            )

        consumers = await self._create_or_get_consumers(
            [order["consumer"] for order in dto["orders"]]
        )
        bill = await self._create_bill(business_id)
        created_orders = self._uow.order_repository.create_many(
            [
                {
                    "id": get_new_id(),
                    "consumer_id": consumer["id"],
                    "business_id": business_id,
                    "bill_id": bill["id"],
                    "latest_time_of_delivery": order["latest_time_of_delivery"],
                    "parcel": order["parcel"],
                    "order_status": OrderStatus.PENDING,
                }
                for consumer, order in zip(consumers, dto["orders"])
            ]
        )

        await self._publish_orders(created_orders, consumers)

        return BaseResponse[list[OrderDto]].success(
            "Order created successfully.",
            [
                OrderDto(
                    **order,
                    consumer=ConsumerDto(**consumer),  # type: ignore
                )
                for order, consumer in zip(created_orders, consumers)
            ],
        )

    async def _publish_orders(
        self, orders: list[Order], consumers: list[Consumer]
    ) -> None:
        for order, consumer in zip(orders, consumers):
            self._producer.publish(
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

    async def _create_or_get_consumers(
        self, consumers: list[ConsumerDto]
    ) -> list[Consumer]:
        return [
            self._uow.consumer_repository.get(phone_number=dto["phone_number"])
            or self._uow.consumer_repository.create(
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
            for dto in consumers
        ]
