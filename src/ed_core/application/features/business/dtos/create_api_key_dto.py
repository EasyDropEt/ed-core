from datetime import UTC, datetime
from uuid import UUID

from ed_domain.core.entities.api_key import ApiKey, ApiKeyStatus
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork
from pydantic import BaseModel

from ed_core.common.generic_helpers import get_new_id


class CreateApiKeyDto(BaseModel):
    name: str
    description: str

    async def create_api_key(
        self,
        business_id: UUID,
        prefix: str,
        key_hash: str,
        uow: ABCAsyncUnitOfWork,
    ) -> ApiKey:
        return await uow.api_key_repository.create(
            ApiKey(
                id=get_new_id(),
                business_id=business_id,
                name=self.name,
                description=self.description,
                prefix=prefix,
                key_hash=key_hash,
                status=ApiKeyStatus.ACTIVE,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
                deleted_datetime=None,
            )
        )
