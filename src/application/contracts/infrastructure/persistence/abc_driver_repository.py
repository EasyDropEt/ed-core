from abc import ABCMeta

from ed_domain_model.entities import Driver

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCDriverRepository(
    ABCGenericRepository[Driver],
    metaclass=ABCMeta,
): ...
