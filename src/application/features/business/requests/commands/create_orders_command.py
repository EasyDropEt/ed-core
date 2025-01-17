from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.business.dtos import CreateOrdersDto, OrderDto


@request(BaseResponse[list[OrderDto]])
@dataclass
class CreateOrdersCommand(Request):
    business_id: UUID
    dto: CreateOrdersDto
