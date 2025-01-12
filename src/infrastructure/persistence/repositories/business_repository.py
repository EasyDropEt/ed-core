from ed_domain_model.entities import Business

from src.application.contracts.infrastructure.persistence.abc_business_repository import (
    ABCBusinessRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class BusinessRepository(GenericRepository[Business], ABCBusinessRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "business")
