from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.dtos import CreateWebhookDto
from ed_core.application.features.common.dtos import WebhookDto


@request(BaseResponse[WebhookDto])
@dataclass
class CreateWebhookCommand(Request):
    business_id: UUID
    dto: CreateWebhookDto
