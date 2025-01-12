from abc import ABCMeta

from ed_domain_model.entities import Bill

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCBillRepository(
    ABCGenericRepository[Bill],
    metaclass=ABCMeta,
): ...
