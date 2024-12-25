from typing import Any, Dict

from requests import Response
from typing_extensions import TypedDict

from ObjectronDecorators.objectron_decorators.decorators import proxy_class


class ResponseMetadata(TypedDict, total=False):
    """Type information for dynamic response metadata."""

    new_field: str


@proxy_class()
class ResponseWrapper:
    def __init__(self, response: Response) -> None:
        self.response = response
        self.metadata: ResponseMetadata = {}
        # Initialize attribute for type checker
        if hasattr(self, "new_field"):
            self.new_field: str

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def json(self) -> Dict[str, Any]:
        return self.response.json()

    def status_code(self) -> int:
        return self.response.status_code
