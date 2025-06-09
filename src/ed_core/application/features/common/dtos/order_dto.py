from datetime import datetime
from uuid import UUID

from ed_domain.core.aggregate_roots.order import OrderStatus, Parcel
from pydantic import BaseModel

from ed_core.application.features.common.dtos import BusinessDto, ConsumerDto
from ed_core.application.features.common.dtos.bill_dto import BillDto


class OrderDto(BaseModel):
    id: UUID
    business: BusinessDto
    consumer: ConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
    bill: BillDto
