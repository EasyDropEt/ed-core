from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos import DriverDto
from src.application.features.driver.dtos import CreateDriverDto


@request(BaseResponse[DriverDto])
@dataclass
class CreateDriverCommand(Request):
    dto: CreateDriverDto
