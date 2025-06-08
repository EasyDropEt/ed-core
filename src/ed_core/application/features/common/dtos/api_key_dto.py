from ed_domain.core.entities.api_key import ApiKeyStatus
from pydantic import BaseModel


class ApiKeyDto(BaseModel):
    name: str
    description: str
    prefix: str
    key_hash: str
    status: ApiKeyStatus
