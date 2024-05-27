from dataclasses import dataclass

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.item import Item


@dataclass
class Result:
    profit: float
    chosen_items: list[Item]
    item_to_capacities: dict[Item, set[CapacityDimension]]

    def __str__(self) -> str:
        return f"Result{{profit={self.profit}, chosenItems={self.chosen_items}}}"
