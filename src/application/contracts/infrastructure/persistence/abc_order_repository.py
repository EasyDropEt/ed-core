from abc import ABCMeta

from ed_domain_model.entities.order import Order

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from src.domain.entities.some_entity import SomeEntity


class ABCOrderRepository(
    ABCGenericRepository[Order],
    metaclass=ABCMeta,
): ...
