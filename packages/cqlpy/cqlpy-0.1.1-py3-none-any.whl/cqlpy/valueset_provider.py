from typing import Protocol


class ValueSetProvider(Protocol):
    def get_valueset(self, name: str, scope: str):
        ...
