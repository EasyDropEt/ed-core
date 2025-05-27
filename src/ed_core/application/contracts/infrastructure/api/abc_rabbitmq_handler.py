from abc import ABCMeta, abstractmethod

from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import \
    ABCAuthRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.abc_notification_rabbitmq_subscriber import \
    ABCNotificationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.abc_optimization_rabbitmq_subscriber import \
    ABCOptimizationRabbitMQSubscriber


class ABCRabbitMQHandler(metaclass=ABCMeta):
    @property
    @abstractmethod
    def optimization_subscriber(self) -> ABCOptimizationRabbitMQSubscriber: ...

    @property
    @abstractmethod
    def notification_subscriber(self) -> ABCNotificationRabbitMQSubscriber: ...

    @property
    @abstractmethod
    def auth_subscriber(self) -> ABCAuthRabbitMQSubscriber: ...
