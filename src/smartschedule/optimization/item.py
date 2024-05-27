from dataclasses import dataclass

from smartschedule.optimization.total_weight import TotalWeight


@dataclass(frozen=True)
class Item:
    name: str
    value: float
    total_weight: TotalWeight

    def is_weight_zero(self) -> bool:
        return len(self.total_weight.components) == 0
