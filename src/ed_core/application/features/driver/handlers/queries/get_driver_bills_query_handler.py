from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import BillDto
from ed_core.application.features.driver.requests.queries import \
    GetDriverBillsQuery


@request_handler(GetDriverBillsQuery, BaseResponse[list[BillDto]])
class GetDriverBillsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetDriverBillsQuery) -> BaseResponse[list[BillDto]]:
        bills = self._uow.bill_repository.get_all(driver_id=request.driver_id)
        if not bills:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Driver bills could not fetched.",
                [f"Bills for driver with id {request.driver_id} not found."],
            )

        return BaseResponse[list[BillDto]].success(
            "Driver bills fetched successfully.",
            [BillDto.from_bill(bill) for bill in bills],
        )
