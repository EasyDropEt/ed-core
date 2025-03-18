from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos import DriverDto


@request(BaseResponse[list[DriverDto]])
@dataclass
class GetAllDriversQuery(Request):
    ...
