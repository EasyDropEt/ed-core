from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.types import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.common.dtos import DeliveryJobDto
from src.application.features.delivery_job.dtos import CreateDeliveryJobDto


@request(BaseResponse[DeliveryJobDto])
@dataclass
class CreateDeliveryJobCommand(Request):
    dto: CreateDeliveryJobDto
