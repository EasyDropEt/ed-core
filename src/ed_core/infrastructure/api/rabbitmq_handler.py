from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import \
    ABCAuthRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.abc_notification_rabbitmq_subscriber import \
    ABCNotificationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.abc_optimization_rabbitmq_subscriber import \
    ABCOptimizationRabbitMQSubscriber

from ed_core.application.contracts.infrastructure.api.abc_rabbitmq_handler import \
    ABCRabbitMQHandler


class RabbitMQHandler(ABCRabbitMQHandler):
    def __init__(
        self,
        auth_subscriber: ABCAuthRabbitMQSubscriber,
        notification_subscriber: ABCNotificationRabbitMQSubscriber,
        optimization_subscriber: ABCOptimizationRabbitMQSubscriber,
    ) -> None:
        self._auth_subscriber = auth_subscriber
        self._notification_subscriber = notification_subscriber
        self._optimization_subscriber = optimization_subscriber

    @property
    def optimization_subscriber(self) -> ABCOptimizationRabbitMQSubscriber:
        return self._optimization_subscriber

    @property
    def notification_subscriber(self) -> ABCNotificationRabbitMQSubscriber:
        return self._notification_subscriber

    @property
    def auth_subscriber(self) -> ABCAuthRabbitMQSubscriber:
        return self._auth_subscriber
