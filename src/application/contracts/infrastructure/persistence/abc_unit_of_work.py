from abc import ABCMeta, abstractmethod

from src.application.contracts.infrastructure.persistence.abc_bill_repository import (
    ABCBillRepository,
)
from src.application.contracts.infrastructure.persistence.abc_business_repository import (
    ABCBusinessRepository,
)
from src.application.contracts.infrastructure.persistence.abc_car_repository import (
    ABCCarRepository,
)
from src.application.contracts.infrastructure.persistence.abc_consumer_repository import (
    ABCConsumerRepository,
)
from src.application.contracts.infrastructure.persistence.abc_delivery_job_repository import (
    ABCDeliveryJobRepository,
)
from src.application.contracts.infrastructure.persistence.abc_driver_repository import (
    ABCDriverRepository,
)
from src.application.contracts.infrastructure.persistence.abc_location_repository import (
    ABCLocationRepository,
)
from src.application.contracts.infrastructure.persistence.abc_order_repository import (
    ABCOrderRepository,
)


class ABCUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def bill_repository(self) -> ABCBillRepository:
        pass

    @property
    @abstractmethod
    def business_repository(self) -> ABCBusinessRepository:
        pass

    @property
    @abstractmethod
    def car_repository(self) -> ABCCarRepository:
        pass

    @property
    @abstractmethod
    def consumer_repository(self) -> ABCConsumerRepository:
        pass

    @property
    @abstractmethod
    def delivery_job_repository(self) -> ABCDeliveryJobRepository:
        pass

    @property
    @abstractmethod
    def driver_repository(self) -> ABCDriverRepository:
        pass

    @property
    @abstractmethod
    def location_repository(self) -> ABCLocationRepository:
        pass

    @property
    @abstractmethod
    def order_repository(self) -> ABCOrderRepository:
        pass
