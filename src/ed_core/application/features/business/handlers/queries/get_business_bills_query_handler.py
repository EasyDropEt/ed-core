from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.requests.queries import \
    GetBusinessBillsQuery
from ed_core.application.features.common.dtos import BillDto


@request_handler(GetBusinessBillsQuery, BaseResponse[list[BillDto]])
class GetBusinessBillsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessBillsQuery
    ) -> BaseResponse[list[BillDto]]:
        bills = self._uow.bill_repository.get_all(
            business_id=request.business_id)
        if not bills:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Business bills could not fetched.",
                [f"Bills for business with id {request.business_id} not found."],
            )

        return BaseResponse[list[BillDto]].success(
            "Business bills fetched successfully.",
            [BillDto.from_bill(bill) for bill in bills],
        )
