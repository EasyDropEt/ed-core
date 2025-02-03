from typing import NotRequired, TypedDict

from src.application.features.common.dtos.business_dto import LocationDto
from src.application.features.common.dtos.car_dto import CarDto


class DriverDto(TypedDict):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    car: CarDto
    location: LocationDto
