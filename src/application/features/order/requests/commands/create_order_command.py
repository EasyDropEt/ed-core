from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.order.dtos.create_order_dto import CreateOrderDto
from src.application.features.order.dtos.order_dto import OrderDto


@request(BaseResponse[OrderDto])
@dataclass
class CreateOrderCommand(Request):
    business_id: UUID
    dto: CreateOrderDto
