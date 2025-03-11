from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos import DriverDto


@request(BaseResponse[DriverDto])
@dataclass
class GetDriverQuery(Request):
    user_id: UUID
