from abc import ABCMeta

from ed_domain_model.entities import Route

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCRouteRepository(
    ABCGenericRepository[Route],
    metaclass=ABCMeta,
): ...
