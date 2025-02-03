from ed_domain_model.entities import DeliveryJob

from src.application.contracts.infrastructure.persistence.abc_delivery_job_repository import (
    ABCDeliveryJobRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class DeliveryJobRepository(GenericRepository[DeliveryJob], ABCDeliveryJobRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "delivery_job")
