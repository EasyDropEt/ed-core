from ed_domain_model.entities import Car

from src.application.contracts.infrastructure.persistence import ABCCarRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class CarRepository(GenericRepository[Car], ABCCarRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "car")
