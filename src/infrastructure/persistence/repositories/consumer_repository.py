from ed_domain_model.entities import Consumer

from src.application.contracts.infrastructure.persistence.abc_consumer_repository import (
    ABCConsumerRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class ConsumerRepository(GenericRepository[Consumer], ABCConsumerRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "consumer")
