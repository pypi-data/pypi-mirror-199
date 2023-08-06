from enum import Enum


class GetTokenPriceAlign(str, Enum):
    VALUE_0 = "5min"
    VALUE_1 = "15min"

    def __str__(self) -> str:
        return str(self.value)
