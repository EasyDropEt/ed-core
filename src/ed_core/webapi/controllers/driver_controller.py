from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.contracts.infrastructure.files.abc_image_uploader import \
    InputImage
from ed_core.application.features.common.dtos.delivery_job_dto import \
    DeliveryJobDto
from ed_core.application.features.common.dtos.driver_dto import DriverDto
from ed_core.application.features.driver.dtos import CreateDriverDto
from ed_core.application.features.driver.requests.commands import (
    CreateDriverCommand, UploadDriverProfilePictureCommand)
from ed_core.application.features.driver.requests.queries import (
    GetDriverDeliveryJobsQuery, GetDriverQuery)
from ed_core.application.features.driver.requests.queries.get_all_drivers_query import \
    GetAllDriversQuery
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Feature"])



@router.get("", response_model=GenericResponse[list[DriverDto]])
@rest_endpoint
async def get_all_drivers(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info("Satisfying get_all_drivers request")
    return await mediator.send(GetAllDriversQuery())


@router.post("", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def create_driver(
    request_dto: CreateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(CreateDriverCommand(dto=request_dto))


@router.get(
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
