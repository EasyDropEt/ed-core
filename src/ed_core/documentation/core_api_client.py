from ed_domain.services.common.api_response import ApiResponse

from ed_core.application.features.business.dtos import (CreateBusinessDto,
                                                        CreateOrderDto,
                                                        OrderDto)
from ed_core.application.features.common.dtos import (BusinessDto,
                                                      DeliveryJobDto,
                                                      DriverDto)
from ed_core.application.features.delivery_job.dtos import CreateDeliveryJobDto
from ed_core.application.features.driver.dtos import CreateDriverDto
from ed_core.common.api_helpers import ApiClient
from ed_core.documentation.abc_core_api_client import ABCCoreApiClient
from ed_core.documentation.endpoints import CoreEndpoint


class CoreApiClient(ABCCoreApiClient):
    def __init__(self, core_api: str) -> None:
        self._endpoints = CoreEndpoint(core_api)

    def create_driver(
        self, create_driver_dto: CreateDriverDto
    ) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("create_driver")
        api_client = ApiClient[DriverDto](endpoint)

        return api_client({"request": create_driver_dto})

    def get_driver_delivery_jobs(
        self, driver_id: str
    ) -> ApiResponse[list[DeliveryJobDto]]:
        endpoint = self._endpoints.get_description("get_driver_delivery_jobs")
        api_client = ApiClient[list[DeliveryJobDto]](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def upload_driver_profile(self, driver_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("upload_driver_profile")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("get_driver")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client({"path_params": {"path_params": {"driver_id": driver_id}}})

    def get_all_businesses(self) -> ApiResponse[list[BusinessDto]]:
        endpoint = self._endpoints.get_description("get_all_businesses")
        api_client = ApiClient[list[BusinessDto]](endpoint)
        return api_client({})

    def create_business(
        self, create_business_dto: CreateBusinessDto
    ) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("create_business")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client({"request": create_business_dto})

    def get_business(self, business_id: str) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("get_business")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client(
            {"path_params": {"path_params": {"business_id": business_id}}}
        )

    def get_business_orders(self, business_id: str) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description("get_business_orders")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client({"path_params": {"business_id": business_id}})

    def create_business_order(
        self, business_id: str, create_order_dto: CreateOrderDto
    ) -> ApiResponse[OrderDto]:
        endpoint = self._endpoints.get_description("create_business_order")
        api_client = ApiClient[OrderDto](endpoint)
        return api_client(
            {"path_params": {"business_id": business_id}, "request": create_order_dto}
        )

    def get_delivery_jobs(self) -> ApiResponse[list[DeliveryJobDto]]:
        endpoint = self._endpoints.get_description("get_delivery_jobs")
        api_client = ApiClient[list[DeliveryJobDto]](endpoint)
        return api_client({})

    def get_delivery_job(self, delivery_job_id: str) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("get_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client({"path_params": {"delivery_job_id": delivery_job_id}})

    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("create_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client({"request": create_delivery_job_dto})
