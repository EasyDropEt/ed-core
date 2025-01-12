from ed_domain_model.entities.order import Order

from src.application.contracts.infrastructure.persistence.abc_order_repository import (
    ABCOrderRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class OrderRepository(GenericRepository[Order], ABCOrderRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "order")
