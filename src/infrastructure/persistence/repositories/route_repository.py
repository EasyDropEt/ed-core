from ed_domain_model.entities.route import Route

from src.application.contracts.infrastructure.persistence import ABCRouteRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class RouteRepository(GenericRepository[Route], ABCRouteRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "route")
