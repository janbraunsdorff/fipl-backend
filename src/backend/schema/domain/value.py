from typing import Final
import math


class Value:
    def __init__(self, value: int):
        if value is None or math.isnan(value):
            value = 0
        self.value: Final[int] = int(value)

    def get_decimal(self) -> str:
        return "{0:.2f}".format(self.value / 100)

    def get_formatted(self) -> str:
        return self.get_decimal() + "€"

    def is_positive(self) -> bool:
        return self.value >= 0
