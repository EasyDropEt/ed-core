from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos.order_dto import ConsumerDto, OrderDto
from src.application.features.business.requests.queries import GetBusinessOrdersQuery


@request_handler(GetBusinessOrdersQuery, BaseResponse[list[OrderDto]])
class GetBusinessOrdersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        return BaseResponse[list[OrderDto]].success(
            "Orders fetched successfully.",
            [
                OrderDto(
                    **order,
                    consumer=ConsumerDto(
                        **self._uow.consumer_repository.get(id=order["consumer_id"]),  # type: ignore
                    ),
                )
                for order in self._uow.order_repository.get_all(
                    business_id=request.business_id
                )
            ],
        )
