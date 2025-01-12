from abc import ABCMeta

from ed_domain_model.entities import Consumer

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCConsumerRepository(
    ABCGenericRepository[Consumer],
    metaclass=ABCMeta,
): ...
