from ed_domain_model.entities import Bill

from src.application.contracts.infrastructure.persistence import ABCBillRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class BillRepository(GenericRepository[Bill], ABCBillRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "bill")
