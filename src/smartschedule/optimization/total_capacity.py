from collections.abc import Sequence
from dataclasses import dataclass

from smartschedule.optimization.capacity_dimension import CapacityDimension


@dataclass(frozen=True)
class TotalCapacity:
    capacities: Sequence[CapacityDimension]

    @staticmethod
    def of(*capacities: CapacityDimension) -> "TotalCapacity":
        return TotalCapacity(list(capacities))

    @staticmethod
    def zero() -> "TotalCapacity":
        return TotalCapacity([])

    def size(self) -> int:
        return len(self.capacities)

    def add(self, capacities: list[CapacityDimension]) -> "TotalCapacity":
        return TotalCapacity(list(self.capacities) + capacities)
