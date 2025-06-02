from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import \
    ABCAuthRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.abc_notification_rabbitmq_subscriber import \
    ABCNotificationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.abc_optimization_rabbitmq_subscriber import \
    ABCOptimizationRabbitMQSubscriber

from ed_core.application.contracts.infrastructure.abc_rabbitmq_producers import \
    ABCRabbitMQProducers


class RabbitMQHandler(ABCRabbitMQProducers):
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
    def optimization(self) -> ABCOptimizationRabbitMQSubscriber:
        return self._optimization_subscriber

    @property
    def notification(self) -> ABCNotificationRabbitMQSubscriber:
        return self._notification_subscriber

    @property
    def auth(self) -> ABCAuthRabbitMQSubscriber:
        return self._auth_subscriber
