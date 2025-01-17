from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.business.dtos import (
    BusinessDto,
    CreateBusinessDto,
    CreateOrdersDto,
    OrderDto,
)
from src.application.features.business.requests.commands import (
    CreateBusinessCommand,
    CreateOrdersCommand,
)
from src.application.features.business.requests.queries import (
    GetAllBusinessQuery,
    GetBusinessByUserIdQuery,
    GetBusinessOrdersQuery,
    GetBusinessQuery,
)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/businesses", tags=["Business Feature"])


@router.get("", response_model=GenericResponse[list[BusinessDto]])
@rest_endpoint
async def get_all_businesses(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetAllBusinessQuery())


@router.post("", response_model=GenericResponse[BusinessDto])
@rest_endpoint
async def create_business(
    request_dto: CreateBusinessDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(CreateBusinessCommand(dto=request_dto))


@router.get("/{business_id}", response_model=GenericResponse[BusinessDto])
@rest_endpoint
async def get_business(
    business_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetBusinessQuery(business_id=business_id))


@router.get("/users/{user_id}", response_model=GenericResponse[BusinessDto])
@rest_endpoint
async def get_business_by_user_id(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetBusinessByUserIdQuery(user_id=user_id))


@router.get("/{business_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def get_business_orders(
    business_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetBusinessOrdersQuery(business_id=business_id))


@router.post("/{business_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def create_order(
    business_id: UUID,
    request_dto: CreateOrdersDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(
        CreateOrdersCommand(business_id=business_id, dto=request_dto)
    )
