from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.business.dtos import BusinessDto, CreateBusinessDto


@request(BaseResponse[BusinessDto])
@dataclass
class CreateBusinessCommand(Request):
    dto: CreateBusinessDto
