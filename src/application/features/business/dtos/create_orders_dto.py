from datetime import datetime
from typing import NotRequired, TypedDict

from ed_domain_model.entities.order import Parcel


class CreateConsumerDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: NotRequired[str]


class CreateOrderDto(TypedDict):
    consumer: CreateConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel


class CreateOrdersDto(TypedDict):
    orders: list[CreateOrderDto]
