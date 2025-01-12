from abc import ABCMeta

from ed_domain_model.entities import Location

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCLocationRepository(
    ABCGenericRepository[Location],
    metaclass=ABCMeta,
): ...
