from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.contracts.infrastructure.files.abc_image_uploader import \
    InputImage
from src.application.features.common.dtos.delivery_job_dto import \
    DeliveryJobDto
from src.application.features.common.dtos.driver_dto import DriverDto
from src.application.features.driver.dtos import CreateDriverDto
from src.application.features.driver.requests.commands import (
    CreateDriverCommand, UploadDriverProfilePictureCommand)
from src.application.features.driver.requests.queries import (
    GetDriverDeliveryJobsQuery, GetDriverQuery)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Feature"])


@router.post("", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def create_driver(
    request_dto: CreateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(CreateDriverCommand(dto=request_dto))


@router.post(
    "/{driver_id}/delivery-jobs", response_model=GenericResponse[list[DeliveryJobDto]]
)
@rest_endpoint
async def driver_delivery_jobs(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id=driver_id))

@router.post(
    "/{driver_id}/upload", response_model=GenericResponse[DriverDto]
)
@rest_endpoint
async def upload_image(
    driver_id: UUID,
    file: UploadFile,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UploadDriverProfilePictureCommand(id=driver_id, file=InputImage(file.file)))

@router.get(
    "/{user_id}", response_model=GenericResponse[DriverDto]
)
@rest_endpoint
async def get_driver_by_user_id(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverQuery(user_id=user_id))
