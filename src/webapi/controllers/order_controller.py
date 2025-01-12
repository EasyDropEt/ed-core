from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.order.dtos import CreateOrderDto, OrderDto
from src.application.features.order.requests.commands import CreateOrderCommand
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/orders", tags=["Order Feature"])


@router.post("/{business_id}", response_model=GenericResponse[OrderDto])
@rest_endpoint
async def post(
    business_id: UUID,
    request_dto: CreateOrderDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(
        CreateOrderCommand(business_id=business_id, dto=request_dto)
    )
