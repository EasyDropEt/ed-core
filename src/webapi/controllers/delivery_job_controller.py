from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.common.dtos import DeliveryJobDto
from src.application.features.delivery_job.dtos import CreateDeliveryJobDto
from src.application.features.delivery_job.requests.commands import (
    CreateDeliveryJobCommand,
)
from src.application.features.delivery_job.requests.queries import GetDeliveryJobsQuery
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/delivery-jobs", tags=["Delivery Job Feature"])


@router.get("", response_model=GenericResponse[list[DeliveryJobDto]])
@rest_endpoint
async def create_driver(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDeliveryJobsQuery())


@router.post("", response_model=GenericResponse[DeliveryJobDto])
@rest_endpoint
async def driver_delivery_jobs(
    dto: CreateDeliveryJobDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateDeliveryJobCommand(dto=dto))
