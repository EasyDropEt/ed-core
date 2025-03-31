from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.route import WayPointType


class WayPointDto(TypedDict):
    order_id: UUID
    type: WayPointType
    eta: datetime
    sequence: int


class RouteDto(TypedDict):
    waypoints: list[WayPointDto]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
