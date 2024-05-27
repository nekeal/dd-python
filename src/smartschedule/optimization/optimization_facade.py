from collections.abc import Sequence
from dataclasses import dataclass

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.item import Item
from smartschedule.optimization.result import Result
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight


@dataclass
class OptimizationFacade:
    def calculate(self, items: list[Item], total_capacity: TotalCapacity) -> Result:
        capacities_size = total_capacity.size()
        dp = [0.0] * (capacities_size + 1)
        chosen_items_list: list[list[Item]] = [[] for _ in range(capacities_size + 1)]
        allocated_capacities_list: list[set[CapacityDimension]] = [
            set() for _ in range(capacities_size + 1)
        ]

        automatically_included_items = [item for item in items if item.is_weight_zero()]
        guaranteed_value = sum(item.value for item in automatically_included_items)

        all_capacities = total_capacity.capacities
        item_to_capacities_map: dict[Item, set[CapacityDimension]] = {}

        for item in sorted(items, key=lambda x: x.value, reverse=True):
            chosen_capacities = self.match_capacities(item.total_weight, all_capacities)
            all_capacities = [
                cap for cap in all_capacities if cap not in chosen_capacities
            ]

            if not chosen_capacities:
                continue

            sum_value = item.value
            chosen_capacities_count = len(chosen_capacities)

            for j in range(capacities_size, chosen_capacities_count - 1, -1):
                if dp[j] < sum_value + dp[j - chosen_capacities_count]:
                    dp[j] = sum_value + dp[j - chosen_capacities_count]
                    chosen_items_list[j] = chosen_items_list[
                        j - chosen_capacities_count
                    ] + [item]
                    allocated_capacities_list[j].update(chosen_capacities)

            item_to_capacities_map[item] = set(chosen_capacities)

        chosen_items_list[capacities_size].extend(automatically_included_items)
        return Result(
            dp[capacities_size] + guaranteed_value,
            chosen_items_list[capacities_size],
            item_to_capacities_map,
        )

    def match_capacities(
        self,
        total_weight: TotalWeight,
        available_capacities: Sequence[CapacityDimension],
    ) -> tuple[CapacityDimension, ...]:
        result = []
        for weight_component in total_weight.components:
            matching_capacity = next(
                (
                    cap
                    for cap in available_capacities
                    if weight_component.is_satisfied_by(cap)
                ),
                None,
            )

            if matching_capacity is not None:
                result.append(matching_capacity)
            else:
                return ()

        return tuple(result)
