from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.files.abc_image_uploader import \
    InputImage
from src.application.features.common.dtos import DriverDto


@request(BaseResponse[DriverDto])
@dataclass
class UploadDriverProfilePictureCommand(Request):
    id: UUID
    file: InputImage
