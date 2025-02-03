from ed_domain_model.entities import Driver

from src.application.contracts.infrastructure.persistence import ABCDriverRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class DriverRepository(GenericRepository[Driver], ABCDriverRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "driver")
