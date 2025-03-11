from dataclasses import dataclass

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.files.abc_image_uploader import \
    ABCImageUploader
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.application.features.common.dtos import DriverDto
from src.application.features.common.dtos.business_dto import LocationDto
from src.application.features.common.dtos.car_dto import CarDto
from src.application.features.driver.requests.commands.upload_driver_profile_picture_command import \
    UploadDriverProfilePictureCommand


@request_handler(UploadDriverProfilePictureCommand, BaseResponse[DriverDto])
@dataclass
class UploadDriverProfilePictureCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, image_uploader: ABCImageUploader):
        self._uow = uow
        self._image_uploader = image_uploader

    async def handle(self, request: UploadDriverProfilePictureCommand) -> BaseResponse[DriverDto]:
        file = await self._image_uploader.upload(request.file)
        if driver := self._uow.driver_repository.get(id=request.id):
            driver['profile_image'] = file['url']
            self._uow.driver_repository.update(driver['id'], driver)

            return BaseResponse[DriverDto].success(
                "Image uploaded successfully.",
                DriverDto(
                    first_name=driver["first_name"],
                    last_name=driver["last_name"],
                    profile_image=driver["profile_image"],
                    phone_number=driver["phone_number"],
                    email=driver.get("email", ""),
                    car=CarDto(**self._uow.car_repository.get(id=driver["car_id"])), # type: ignore
                    location=LocationDto(**self._uow.location_repository.get(id=driver["location_id"])),# type: ignore
                )
            )

        return BaseResponse[DriverDto].error("Image couldn't be uploaded.", ["Driver with id {request.id} does not exist."])
