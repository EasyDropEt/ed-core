from abc import ABCMeta

from ed_domain_model.entities import Business

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCBusinessRepository(
    ABCGenericRepository[Business],
    metaclass=ABCMeta,
): ...
