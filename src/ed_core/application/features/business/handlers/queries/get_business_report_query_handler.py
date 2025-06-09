from typing import Callable

from ed_domain.core.aggregate_roots import Order
from ed_domain.core.aggregate_roots.order import OrderStatus
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.dtos import BusinessReportDto
from ed_core.application.features.business.requests.queries import \
    GetBusinessReportQuery
from ed_core.application.features.common.dtos.order_dto import OrderDto
from ed_core.application.services.order_service import OrderService


@request_handler(GetBusinessReportQuery, BaseResponse[BusinessReportDto])
class GetBusinessReportQueryHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork):
        self._uow = uow
        self._order_service = OrderService(uow)

    async def handle(
        self, request: GetBusinessReportQuery
    ) -> BaseResponse[BusinessReportDto]:
        async with self._uow.transaction():
            orders = await self._uow.order_repository.get_all(
                business_id=request.business_id
            )
            report = await self._generate_report(orders)

        return BaseResponse[BusinessReportDto].success(
            "Business fetched successfully.", report
        )

    async def _generate_report(self, orders: list[Order]) -> BusinessReportDto:
        total_orders = len(orders)
        completed_deliveries = self._count(
            orders, lambda x: x.order_status == OrderStatus.COMPLETED
        )
        cancelled_deliveries = self._count(
            orders, lambda x: x.order_status == OrderStatus.CANCELLED
        )
        failed_deliveries = self._count(
            orders, lambda x: x.order_status == OrderStatus.FAILED
        )
        pending_deliveries = self._count(
            orders, lambda x: x.order_status == OrderStatus.PENDING
        )

        return BusinessReportDto(
            orders=[await self._order_service.to_dto(order) for order in orders],
            total_orders=total_orders,
            completed_deliveries=completed_deliveries,
            cancelled_deliveries=cancelled_deliveries,
            failed_deliveries=failed_deliveries,
            pending_deliveries=pending_deliveries,
            average_order_value_birr=self._average(
                [order.bill.amount_in_birr for order in orders]
            ),
            total_revenue_birr=sum(
                [order.bill.amount_in_birr for order in orders]),
        )

    def _count(self, orders: list[Order], fn: Callable[[Order], bool]) -> int:
        return sum(fn(order) for order in orders)

    def _average(self, values: list[float]) -> float:
        return round(sum(values) / len(values), 2)
