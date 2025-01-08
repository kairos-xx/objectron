from typing import Dict

from objectron_decorators.decorators import proxy_class


@proxy_class()
class FeatureFlags:
    def __init__(self, flags: Dict[str, bool]) -> None:
        self.flags = flags

    def enable(self, feature: str) -> bool:
        self.flags[feature] = True
        return self.flags[feature]

    def disable(self, feature: str) -> bool:
        self.flags[feature] = False
        return self.flags[feature]

    def is_enabled(self, feature: str) -> bool:
        return self.flags.get(feature, False)
