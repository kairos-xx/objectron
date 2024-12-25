from typing import TypedDict

from objectron_decorators.decorators import proxy_class


class Credentials(TypedDict):
    username: str
    password: str


class DatabaseConfig(TypedDict):
    credentials: Credentials
    host: str
    port: int


@proxy_class()
class Configuration:
    def __init__(self):
        self.database: DatabaseConfig = {
            "credentials": {"username": "", "password": ""},
            "host": "",
            "port": 0,
        }

    def setup(self):
        self.database["host"] = "localhost"
        self.database["port"] = 5432
        self.database["credentials"]["username"] = "admin"
        self.database["credentials"]["password"] = "secret"


config = Configuration()
config.setup()
print(config.database["credentials"]["username"])  # "admin"
