from typing import Any

from objectron_decorators.decorators import proxy_class


@proxy_class()
class User:
    def __init__(self, name: str):
        self.name = name
        self.age = 0
        self.location: str = ""
        self.__dict__: dict[str, Any] = {}

    def set_age(self, age: int) -> None:
        self.age = age

    def get_info(self) -> str:
        return f"{self.name} is {self.age} years old"


# Usage
user = User("John")
user.set_age(25)
print(user.get_info())
user.location = "New York"  # Dynamic attribute creation
