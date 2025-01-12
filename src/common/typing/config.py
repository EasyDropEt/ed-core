from typing import TypedDict


class Config(TypedDict):
    mongo_db_connection_string: str
    db_name: str


class TestMessage(TypedDict):
    title: str
