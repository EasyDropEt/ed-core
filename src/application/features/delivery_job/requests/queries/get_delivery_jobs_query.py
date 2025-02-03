from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.types import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos import DeliveryJobDto


@request(BaseResponse[list[DeliveryJobDto]])
@dataclass
class GetDeliveryJobsQuery(Request): ...
