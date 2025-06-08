from pydantic import BaseModel

from ed_core.application.features.common.dtos.order_dto import OrderDto


class BusinessReportDto(BaseModel):
    orders: list[OrderDto]

    total_orders: int
    completed_deliveries: int
    cancelled_deliveries: int
    pending_deliveries: int
    failed_deliveries: int

    total_revenue_birr: float
    average_order_value_birr: float

    # report_start_date: datetime
    # report_end_date: datetime

    # average_delivery_time_minutes: float
    #
    # average_delivery_distance_km: float
    # on_time_delivery_rate: float
    # late_deliveries: int
    #
    # customer_satisfaction_average_rating: float
    # new_customers: int
    # repeat_customers: int
    #
    # average_driver_rating: Optional[float]  # Overall average driver rating
    #
    # # Hour of day -> Number of deliveries
    # peak_delivery_hours: Optional[dict[str, int]]
    # # Day of week -> Number of deliveries
    # peak_delivery_days: Optional[dict[str, int]]
