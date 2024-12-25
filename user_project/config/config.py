from typing import Any

from ObjectronDecorators.objectron_decorators.decorators import proxy_class


@proxy_class()
class AppConfig:
    def __init__(self, db_host: str, db_port: int, debug: bool = False) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.debug = debug

    def toggle_debug(self) -> bool:
        self.debug = not self.debug
        return self.debug

    def _is_path_string(self, path: str) -> bool:
        return "." in path

    def _resolve_path(self, path: str, create: bool = False) -> tuple[dict, str]:
        current = self.__dict__
        parts = path.split(".")

        for part in parts[:-1]:
            if part not in current and create:
                current[part] = {}
            current = current[part]
        return current, parts[-1]

    def __getitem__(self, key: str) -> Any:
        if self._is_path_string(key):
            current, last_part = self._resolve_path(key)
            return current[last_part]
        return self.__dict__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if self._is_path_string(key):
            current, last_part = self._resolve_path(key, create=True)
            current[last_part] = value
        else:
            self.__dict__[key] = value

    def __getattr__(self, name: str) -> Any:
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )
