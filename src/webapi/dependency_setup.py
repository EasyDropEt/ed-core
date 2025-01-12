from rmediator.mediator import Mediator

from src.application.features.business.handlers.commands import (
    CreateBusinessCommandHandler,
)
from src.application.features.business.requests.commands import CreateBusinessCommand
from src.application.features.driver.handlers.commands import CreateDriverCommandHandler
from src.application.features.driver.requests.commands import CreateDriverCommand
from src.application.features.order.handlers.commands import CreateOrderCommandHandler
from src.application.features.order.requests.commands import CreateOrderCommand
from src.common.generic_helpers import get_config
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def mediator() -> Mediator:
    # Dependencies
    config = get_config()
    print(config)

    db_client = DbClient(
        config["mongo_db_connection_string"],
        config["db_name"],
    )
    uow = UnitOfWork(db_client)

    # Setup
    mediator = Mediator()

    handlers = [
        # Order handler
        (CreateOrderCommand, CreateOrderCommandHandler(uow)),
        # Driver handlers
        (CreateDriverCommand, CreateDriverCommandHandler(uow)),
        # Business handlers
        (CreateBusinessCommand, CreateBusinessCommandHandler(uow)),
    ]
    for command, handler in handlers:
        mediator.register_handler(command, handler)

    db_client.start()
    return mediator
