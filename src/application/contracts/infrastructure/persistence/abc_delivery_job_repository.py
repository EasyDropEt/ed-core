from abc import ABCMeta

from ed_domain_model.entities import DeliveryJob

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCDeliveryJobRepository(
    ABCGenericRepository[DeliveryJob],
    metaclass=ABCMeta,
): ...
