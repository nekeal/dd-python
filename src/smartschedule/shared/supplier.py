from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Supplier(Generic[T]):
    """Port of Supplier from Java"""

    func: Callable[[], T]

    def get(self) -> T:
        return self.func()
