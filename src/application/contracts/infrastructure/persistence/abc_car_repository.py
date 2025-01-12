from abc import ABCMeta

from ed_domain_model.entities import Car

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCCarRepository(
    ABCGenericRepository[Car],
    metaclass=ABCMeta,
): ...
