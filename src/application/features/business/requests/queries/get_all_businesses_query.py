from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos.business_dto import BusinessDto


@request(BaseResponse[list[BusinessDto]])
@dataclass
class GetAllBusinessQuery(Request): ...
