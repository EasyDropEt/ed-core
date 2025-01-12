from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.order.dtos.order_dto import OrderDto


@request(BaseResponse[list[OrderDto]])
@dataclass
class GetBusinessOrdersQuery(Request):
    business_id: UUID
