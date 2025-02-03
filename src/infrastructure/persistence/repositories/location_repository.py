from ed_domain_model.entities.location import Location

from src.application.contracts.infrastructure.persistence import ABCLocationRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class LocationRepository(GenericRepository[Location], ABCLocationRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "location")
