from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import \
    ABCAuthRabbitMQSubscriber
from ed_auth.documentation.message_queue.rabbitmq.auth_rabbitmq_subscriber import \
    AuthRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.abc_notification_rabbitmq_subscriber import \
    ABCNotificationRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.notification_rabbitmq_subscriber import \
    NotificationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.abc_optimization_rabbitmq_subscriber import \
    ABCOptimizationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.optimization_rabbitmq_subscriber import \
    OptimizationRabbitMQSubscriber

from ed_core.application.contracts.infrastructure.abc_rabbitmq_producers import \
    ABCRabbitMQProducers
from ed_core.common.typing.config import RabbitMQConfig


class RabbitMQHandler(ABCRabbitMQProducers):
    def __init__(self, config: RabbitMQConfig) -> None:
        self._auth_subscriber = AuthRabbitMQSubscriber(config["url"])
        self._notification_subscriber = NotificationRabbitMQSubscriber(
            config["url"])
        self._optimization_subscriber = OptimizationRabbitMQSubscriber(
            config["url"])

    async def start(self):
        await self._auth_subscriber.start()
        await self._notification_subscriber.start()

    @property
    def optimization(self) -> ABCOptimizationRabbitMQSubscriber:
        return self._optimization_subscriber

    @property
    def notification(self) -> ABCNotificationRabbitMQSubscriber:
        return self._notification_subscriber

    @property
    def auth(self) -> ABCAuthRabbitMQSubscriber:
        return self._auth_subscriber
